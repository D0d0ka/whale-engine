from WhaleEngine.logging import logLn
from WhaleEngine.color import Color
from WhaleEngine.keys import KeyAction, Keys, MouseButtons

from vulkan import *

import sys
import math
import time
import glfw
import numpy as np

# KHR procedure names are loaded dynamically via vkGet*ProcAddr at runtime.
vkGetPhysicalDeviceSurfaceSupportKHR = None
vkGetPhysicalDeviceSurfaceCapabilitiesKHR = None
vkGetPhysicalDeviceSurfaceFormatsKHR = None
vkGetPhysicalDeviceSurfacePresentModesKHR = None
vkCreateSwapchainKHR = None
vkGetSwapchainImagesKHR = None
vkAcquireNextImageKHR = None
vkQueuePresentKHR = None
vkDestroySwapchainKHR = None
vkDestroySurfaceKHR = None


class windowAPI:
    def __init__(
        self,
        title="Whale Engine (Vulkan)",
        width=800,
        height=600,
        color=Color(0.1, 0.1, 0.1, 1),
        target_fps=None,
    ):
        if not glfw.init():
            logLn("GLFW initialization failed.")
            sys.exit(1)

        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)

        self.width = width
        self.height = height
        self.title = title
        self._color = color

        self.handle = glfw.create_window(width, height, title, None, None)
        if not self.handle:
            glfw.terminate()
            logLn("Vulkan window creation failed.")
            sys.exit(1)

        glfw.set_framebuffer_size_callback(self.handle, self._resize)
        glfw.set_key_callback(self.handle, self._on_key)

        self.keys = {}
        self.key_callbacks = []

        self._framebuffer_resized = False
        self._terminated = False
        self._pending_entities = []
        self._camera = None
        self._next_texture_id = 1
        self._textures = {}
        self._recovering = False
        self._fence_wait_timeout_ns = 100_000_000

        # Single frame in flight is slower but significantly more stable for this minimal backend.
        self._max_frames_in_flight = 1
        self._current_frame = 0

        self._target_fps = target_fps
        self._last_frame_time = time.perf_counter()
        self._create_vulkan_context()
        logLn("Vulkan window loaded.", "window")

    # Public API parity
    def set_size(self, width, height):
        self.width = width
        self.height = height
        glfw.set_window_size(self.handle, width, height)

    def set_width(self, width):
        self.set_size(width, self.height)

    def set_height(self, height):
        self.set_size(self.width, height)

    def set_title(self, title):
        self.title = title
        glfw.set_window_title(self.handle, title)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self.set_color(value)

    def set_color(self, color):
        self._color = color

    def set_target_fps(self, fps):
        self._target_fps = fps

    def _precise_sleep_until(self, deadline):
        """Hybrid sleep+spin to hit `deadline` (perf_counter) with ~0.1ms accuracy."""
        remaining = deadline - time.perf_counter()
        if remaining > 0.002:
            time.sleep(remaining - 0.002)
        while time.perf_counter() < deadline:
            pass

    def poll(self):
        glfw.poll_events()

    def clear(self):
        # Clear happens during Vulkan render pass in swap().
        pass

    def swap(self):
        try:
            self._draw_frame()
        except VkErrorOutOfDateKhr:
            self._recreate_swapchain()
        except VkErrorDeviceLost:
            logLn("Vulkan device lost, attempting renderer recovery.", "error logger")
            self._recover_vulkan_renderer()
        except Exception as exc:
            logLn(f"Vulkan draw error: {exc}", "error logger")
            self._recover_vulkan_renderer()
        if self._target_fps is not None and self._target_fps > 0:
            deadline = self._last_frame_time + 1.0 / self._target_fps
            self._precise_sleep_until(deadline)
            self._last_frame_time = deadline
        else:
            self._last_frame_time = time.perf_counter()

    def should_close(self):
        return glfw.window_should_close(self.handle)

    def request_close(self):
        glfw.set_window_should_close(self.handle, True)

    def terminate(self):
        if self._terminated:
            return
        self._terminated = True
        self._cleanup()
        logLn("Window closed.", "window")
        glfw.terminate()
        sys.exit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.terminate()
        return False

    def normalize_key(self, key):
        if isinstance(key, str):
            return key
        return self._key_name_from_native(key)

    def set_key_callback(self, callback):
        self.key_callbacks.append(callback)

    def remove_key_callback(self, callback):
        if callback in self.key_callbacks:
            self.key_callbacks.remove(callback)

    def is_key_down(self, key):
        return self.keys.get(self.normalize_key(key), False)

    def get_cursor_pos(self):
        return glfw.get_cursor_pos(self.handle)

    def set_cursor_pos(self, x, y):
        glfw.set_cursor_pos(self.handle, x, y)

    def _normalize_mouse_button(self, button):
        if button == MouseButtons.LEFT:
            return glfw.MOUSE_BUTTON_LEFT
        if button == MouseButtons.RIGHT:
            return glfw.MOUSE_BUTTON_RIGHT
        if button == MouseButtons.MIDDLE:
            return glfw.MOUSE_BUTTON_MIDDLE
        if isinstance(button, int):
            return button
        raise ValueError(f"Unknown mouse button: {button}")

    def is_mouse_button_down(self, button):
        native_button = self._normalize_mouse_button(button)
        return glfw.get_mouse_button(self.handle, native_button) == glfw.PRESS

    def create_texture_from_image(self, image):
        # Texture upload path is separate; keeping API stable for engine users.
        img = image.convert("RGBA")
        tex_id = self._next_texture_id
        self._next_texture_id += 1
        pixels_np = np.frombuffer(img.tobytes(), dtype=np.uint8).reshape((img.size[1], img.size[0], 4)).copy()
        self._textures[tex_id] = {
            "width": img.size[0],
            "height": img.size[1],
            "pixels_np": pixels_np,
        }
        return tex_id

    def render_2d_entities(self, entities, camera):
        self._pending_entities = entities
        self._camera = camera

    # Input helpers
    def _action_name_from_native(self, action):
        if action == glfw.PRESS:
            return KeyAction.PRESS
        if action == glfw.REPEAT:
            return KeyAction.REPEAT
        if action == glfw.RELEASE:
            return KeyAction.RELEASE
        return str(action)

    def _key_name_from_native(self, key):
        named_keys = {
            glfw.KEY_UP: Keys.UP,
            glfw.KEY_DOWN: Keys.DOWN,
            glfw.KEY_LEFT: Keys.LEFT,
            glfw.KEY_RIGHT: Keys.RIGHT,
            glfw.KEY_SPACE: Keys.SPACE,
            glfw.KEY_ESCAPE: Keys.ESCAPE,
            glfw.KEY_ENTER: Keys.ENTER,
            glfw.KEY_TAB: Keys.TAB,
            glfw.KEY_BACKSPACE: Keys.BACKSPACE,
            glfw.KEY_LEFT_SHIFT: Keys.LEFT_SHIFT,
            glfw.KEY_RIGHT_SHIFT: Keys.RIGHT_SHIFT,
            glfw.KEY_LEFT_CONTROL: Keys.LEFT_CTRL,
            glfw.KEY_RIGHT_CONTROL: Keys.RIGHT_CTRL,
            glfw.KEY_LEFT_ALT: Keys.LEFT_ALT,
            glfw.KEY_RIGHT_ALT: Keys.RIGHT_ALT,
            glfw.KEY_INSERT: Keys.INSERT,
            glfw.KEY_HOME: Keys.HOME,
            glfw.KEY_PAGE_UP: Keys.PAGE_UP,
            glfw.KEY_DELETE: Keys.DELETE,
            glfw.KEY_END: Keys.END,
            glfw.KEY_PAGE_DOWN: Keys.PAGE_DOWN,
            glfw.KEY_F1: Keys.F1,
            glfw.KEY_F2: Keys.F2,
            glfw.KEY_F3: Keys.F3,
            glfw.KEY_F4: Keys.F4,
            glfw.KEY_F5: Keys.F5,
            glfw.KEY_F6: Keys.F6,
            glfw.KEY_F7: Keys.F7,
            glfw.KEY_F8: Keys.F8,
            glfw.KEY_F9: Keys.F9,
            glfw.KEY_F10: Keys.F10,
            glfw.KEY_F11: Keys.F11,
            glfw.KEY_F12: Keys.F12,
            glfw.KEY_0: Keys.NUMBER_0,
            glfw.KEY_1: Keys.NUMBER_1,
            glfw.KEY_2: Keys.NUMBER_2,
            glfw.KEY_3: Keys.NUMBER_3,
            glfw.KEY_4: Keys.NUMBER_4,
            glfw.KEY_5: Keys.NUMBER_5,
            glfw.KEY_6: Keys.NUMBER_6,
            glfw.KEY_7: Keys.NUMBER_7,
            glfw.KEY_8: Keys.NUMBER_8,
            glfw.KEY_9: Keys.NUMBER_9,
            glfw.KEY_KP_0: Keys.NUMPAD_0,
            glfw.KEY_KP_1: Keys.NUMPAD_1,
            glfw.KEY_KP_2: Keys.NUMPAD_2,
            glfw.KEY_KP_3: Keys.NUMPAD_3,
            glfw.KEY_KP_4: Keys.NUMPAD_4,
            glfw.KEY_KP_5: Keys.NUMPAD_5,
            glfw.KEY_KP_6: Keys.NUMPAD_6,
            glfw.KEY_KP_7: Keys.NUMPAD_7,
            glfw.KEY_KP_8: Keys.NUMPAD_8,
            glfw.KEY_KP_9: Keys.NUMPAD_9,
        }
        if key in named_keys:
            return named_keys[key]

        if glfw.KEY_A <= key <= glfw.KEY_Z:
            return chr(ord("a") + (key - glfw.KEY_A))

        return f"key_{key}"

    def _on_key(self, window, key, scancode, action, mods):
        key_name = self._key_name_from_native(key)
        action_name = self._action_name_from_native(action)

        if action_name in (KeyAction.PRESS, KeyAction.REPEAT):
            self.keys[key_name] = True
        elif action_name == KeyAction.RELEASE:
            self.keys[key_name] = False

        for callback in self.key_callbacks:
            callback(window, key_name, scancode, action_name, mods)

    def _resize(self, window, w, h):
        fw, fh = glfw.get_framebuffer_size(self.handle)
        self.width = fw if fw > 0 else w
        self.height = fh if fh > 0 else h
        self._framebuffer_resized = True

    # Vulkan setup
    def _create_vulkan_context(self):
        self._create_instance()
        self._create_surface()
        self._load_instance_level_functions()
        self._pick_physical_device()
        self._create_logical_device()
        self._load_device_level_functions()
        self._create_swapchain_and_dependents()
        self._create_software_framebuffer_resources()
        self._create_command_pool()
        self._create_command_buffers()
        self._create_sync_objects()

    def _load_instance_level_functions(self):
        self.vkGetPhysicalDeviceSurfaceSupportKHR = vkGetInstanceProcAddr(self.instance, "vkGetPhysicalDeviceSurfaceSupportKHR")
        self.vkGetPhysicalDeviceSurfaceCapabilitiesKHR = vkGetInstanceProcAddr(self.instance, "vkGetPhysicalDeviceSurfaceCapabilitiesKHR")
        self.vkGetPhysicalDeviceSurfaceFormatsKHR = vkGetInstanceProcAddr(self.instance, "vkGetPhysicalDeviceSurfaceFormatsKHR")
        self.vkGetPhysicalDeviceSurfacePresentModesKHR = vkGetInstanceProcAddr(self.instance, "vkGetPhysicalDeviceSurfacePresentModesKHR")
        self.vkDestroySurfaceKHR = vkGetInstanceProcAddr(self.instance, "vkDestroySurfaceKHR")

    def _load_device_level_functions(self):
        self.vkCreateSwapchainKHR = vkGetDeviceProcAddr(self.device, "vkCreateSwapchainKHR")
        self.vkDestroySwapchainKHR = vkGetDeviceProcAddr(self.device, "vkDestroySwapchainKHR")
        self.vkGetSwapchainImagesKHR = vkGetDeviceProcAddr(self.device, "vkGetSwapchainImagesKHR")
        self.vkAcquireNextImageKHR = vkGetDeviceProcAddr(self.device, "vkAcquireNextImageKHR")
        self.vkQueuePresentKHR = vkGetDeviceProcAddr(self.device, "vkQueuePresentKHR")

    def _create_instance(self):
        app_info = VkApplicationInfo(
            sType=VK_STRUCTURE_TYPE_APPLICATION_INFO,
            pApplicationName=self.title,
            applicationVersion=VK_MAKE_VERSION(1, 0, 0),
            pEngineName="WhaleEngine",
            engineVersion=VK_MAKE_VERSION(1, 0, 0),
            apiVersion=VK_API_VERSION_1_0,
        )

        exts = glfw.get_required_instance_extensions()
        if exts is None:
            raise RuntimeError("GLFW did not provide required Vulkan instance extensions.")

        ext_count = len(exts)

        create_info = VkInstanceCreateInfo(
            sType=VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
            pApplicationInfo=app_info,
            enabledExtensionCount=ext_count,
            ppEnabledExtensionNames=exts,
            enabledLayerCount=0,
            ppEnabledLayerNames=None,
        )

        self.instance = vkCreateInstance(create_info, None)

    def _create_surface(self):
        surface_ptr = ffi.new("VkSurfaceKHR[1]")
        result = glfw.create_window_surface(self.instance, self.handle, None, surface_ptr)
        if result != VK_SUCCESS:
            raise RuntimeError(f"glfwCreateWindowSurface failed with VkResult={result}.")

        self.surface = surface_ptr[0]
        if self.surface == VK_NULL_HANDLE:
            raise RuntimeError("Failed to create Vulkan surface.")

    def _pick_physical_device(self):
        devices = vkEnumeratePhysicalDevices(self.instance)
        if not devices:
            raise RuntimeError("No Vulkan-capable GPU found.")

        for dev in devices:
            indices = self._find_queue_families(dev)
            if self._is_device_suitable(dev, indices):
                self.physical_device = dev
                self._queue_family_indices = indices
                return

        raise RuntimeError("No suitable Vulkan GPU found.")

    def _is_device_suitable(self, device, indices):
        if indices["graphics"] is None or indices["present"] is None:
            return False

        # This minimal renderer records/executes copy on graphics queue and then presents.
        # Restricting to unified queue families avoids ownership-transfer complexity.
        if indices["graphics"] != indices["present"]:
            return False

        avail_exts = vkEnumerateDeviceExtensionProperties(device, None)
        avail_names = {ext.extensionName for ext in avail_exts}
        if VK_KHR_SWAPCHAIN_EXTENSION_NAME not in avail_names:
            return False

        support = self._query_swapchain_support(device)
        return bool(support["formats"]) and bool(support["present_modes"])

    def _find_queue_families(self, device):
        families = vkGetPhysicalDeviceQueueFamilyProperties(device)
        result = {"graphics": None, "present": None}

        for i, fam in enumerate(families):
            if fam.queueCount > 0 and (fam.queueFlags & VK_QUEUE_GRAPHICS_BIT):
                result["graphics"] = i

            present_support = self.vkGetPhysicalDeviceSurfaceSupportKHR(device, i, self.surface)
            if present_support:
                result["present"] = i

            if result["graphics"] is not None and result["present"] is not None:
                break

        return result

    def _create_logical_device(self):
        unique_families = {self._queue_family_indices["graphics"], self._queue_family_indices["present"]}

        queue_priority = [1.0]
        queue_infos = []
        for qf in unique_families:
            queue_infos.append(
                VkDeviceQueueCreateInfo(
                    sType=VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO,
                    queueFamilyIndex=qf,
                    queueCount=1,
                    pQueuePriorities=queue_priority,
                )
            )

        device_features = VkPhysicalDeviceFeatures()

        create_info = VkDeviceCreateInfo(
            sType=VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO,
            queueCreateInfoCount=len(queue_infos),
            pQueueCreateInfos=queue_infos,
            enabledExtensionCount=1,
            ppEnabledExtensionNames=[VK_KHR_SWAPCHAIN_EXTENSION_NAME],
            pEnabledFeatures=device_features,
            enabledLayerCount=0,
            ppEnabledLayerNames=None,
        )

        self.device = vkCreateDevice(self.physical_device, create_info, None)
        self.graphics_queue = vkGetDeviceQueue(self.device, self._queue_family_indices["graphics"], 0)
        self.present_queue = vkGetDeviceQueue(self.device, self._queue_family_indices["present"], 0)

    def _query_swapchain_support(self, device):
        capabilities = self.vkGetPhysicalDeviceSurfaceCapabilitiesKHR(device, self.surface)
        formats = self.vkGetPhysicalDeviceSurfaceFormatsKHR(device, self.surface)
        present_modes = self.vkGetPhysicalDeviceSurfacePresentModesKHR(device, self.surface)
        return {
            "capabilities": capabilities,
            "formats": formats,
            "present_modes": present_modes,
        }

    def _choose_swap_surface_format(self, formats):
        for fmt in formats:
            if fmt.format == VK_FORMAT_B8G8R8A8_SRGB and fmt.colorSpace == VK_COLOR_SPACE_SRGB_NONLINEAR_KHR:
                return fmt
        return formats[0]

    def _choose_present_mode(self, present_modes):
        for mode in present_modes:
            if mode == VK_PRESENT_MODE_MAILBOX_KHR:
                return mode
        return VK_PRESENT_MODE_FIFO_KHR

    def _choose_extent(self, capabilities):
        if capabilities.currentExtent.width != 0xFFFFFFFF:
            return capabilities.currentExtent

        w, h = glfw.get_framebuffer_size(self.handle)
        width = max(capabilities.minImageExtent.width, min(capabilities.maxImageExtent.width, w))
        height = max(capabilities.minImageExtent.height, min(capabilities.maxImageExtent.height, h))
        return VkExtent2D(width=width, height=height)

    def _create_swapchain_and_dependents(self):
        support = self._query_swapchain_support(self.physical_device)
        surface_format = self._choose_swap_surface_format(support["formats"])
        present_mode = self._choose_present_mode(support["present_modes"])
        extent = self._choose_extent(support["capabilities"])

        image_count = support["capabilities"].minImageCount + 1
        if support["capabilities"].maxImageCount > 0 and image_count > support["capabilities"].maxImageCount:
            image_count = support["capabilities"].maxImageCount

        graphics_family = self._queue_family_indices["graphics"]
        present_family = self._queue_family_indices["present"]

        if graphics_family != present_family:
            sharing_mode = VK_SHARING_MODE_CONCURRENT
            family_indices = [graphics_family, present_family]
            family_count = 2
        else:
            sharing_mode = VK_SHARING_MODE_EXCLUSIVE
            family_indices = None
            family_count = 0

        create_info = VkSwapchainCreateInfoKHR(
            sType=VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR,
            surface=self.surface,
            minImageCount=image_count,
            imageFormat=surface_format.format,
            imageColorSpace=surface_format.colorSpace,
            imageExtent=extent,
            imageArrayLayers=1,
            imageUsage=VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT | VK_IMAGE_USAGE_TRANSFER_DST_BIT,
            imageSharingMode=sharing_mode,
            queueFamilyIndexCount=family_count,
            pQueueFamilyIndices=family_indices,
            preTransform=support["capabilities"].currentTransform,
            compositeAlpha=VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR,
            presentMode=present_mode,
            clipped=True,
            oldSwapchain=VK_NULL_HANDLE,
        )

        self.swapchain = self.vkCreateSwapchainKHR(self.device, create_info, None)
        self.swapchain_images = self.vkGetSwapchainImagesKHR(self.device, self.swapchain)
        self.swapchain_image_format = surface_format.format
        self.swapchain_extent = extent
        self._image_initialized = [False for _ in self.swapchain_images]
        self._swapchain_is_bgra = self.swapchain_image_format in (
            VK_FORMAT_B8G8R8A8_UNORM,
            VK_FORMAT_B8G8R8A8_SRGB,
        )

    def _find_memory_type(self, type_filter, properties):
        mem_properties = vkGetPhysicalDeviceMemoryProperties(self.physical_device)
        for i in range(mem_properties.memoryTypeCount):
            if (type_filter & (1 << i)) and (mem_properties.memoryTypes[i].propertyFlags & properties) == properties:
                return i
        raise RuntimeError("No compatible Vulkan memory type found.")

    def _create_software_framebuffer_resources(self):
        self._fb_width = int(self.swapchain_extent.width)
        self._fb_height = int(self.swapchain_extent.height)
        self._fb_size = self._fb_width * self._fb_height * 4
        self._cpu_framebuffer_np = np.zeros((self._fb_height, self._fb_width, 4), dtype=np.uint8)
        self._cpu_framebuffer = self._cpu_framebuffer_np.reshape(-1)

        buffer_info = VkBufferCreateInfo(
            sType=VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO,
            size=self._fb_size,
            usage=VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
            sharingMode=VK_SHARING_MODE_EXCLUSIVE,
        )
        self._staging_buffer = vkCreateBuffer(self.device, buffer_info, None)
        reqs = vkGetBufferMemoryRequirements(self.device, self._staging_buffer)

        alloc_info = VkMemoryAllocateInfo(
            sType=VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO,
            allocationSize=reqs.size,
            memoryTypeIndex=self._find_memory_type(
                reqs.memoryTypeBits,
                VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT,
            ),
        )
        self._staging_memory = vkAllocateMemory(self.device, alloc_info, None)
        vkBindBufferMemory(self.device, self._staging_buffer, self._staging_memory, 0)

    def _destroy_software_framebuffer_resources(self):
        if getattr(self, "_staging_buffer", None):
            vkDestroyBuffer(self.device, self._staging_buffer, None)
            self._staging_buffer = None
        if getattr(self, "_staging_memory", None):
            vkFreeMemory(self.device, self._staging_memory, None)
            self._staging_memory = None
        self._cpu_framebuffer_np = None
        self._cpu_framebuffer = None
        self._fb_width = 0
        self._fb_height = 0
        self._fb_size = 0

    def _create_image_views(self):
        self.swapchain_image_views = []

        for image in self.swapchain_images:
            create_info = VkImageViewCreateInfo(
                sType=VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO,
                image=image,
                viewType=VK_IMAGE_VIEW_TYPE_2D,
                format=self.swapchain_image_format,
                components=VkComponentMapping(
                    r=VK_COMPONENT_SWIZZLE_IDENTITY,
                    g=VK_COMPONENT_SWIZZLE_IDENTITY,
                    b=VK_COMPONENT_SWIZZLE_IDENTITY,
                    a=VK_COMPONENT_SWIZZLE_IDENTITY,
                ),
                subresourceRange=VkImageSubresourceRange(
                    aspectMask=VK_IMAGE_ASPECT_COLOR_BIT,
                    baseMipLevel=0,
                    levelCount=1,
                    baseArrayLayer=0,
                    layerCount=1,
                ),
            )
            self.swapchain_image_views.append(vkCreateImageView(self.device, create_info, None))

    def _create_render_pass(self):
        color_attachment = VkAttachmentDescription(
            format=self.swapchain_image_format,
            samples=VK_SAMPLE_COUNT_1_BIT,
            loadOp=VK_ATTACHMENT_LOAD_OP_CLEAR,
            storeOp=VK_ATTACHMENT_STORE_OP_STORE,
            stencilLoadOp=VK_ATTACHMENT_LOAD_OP_DONT_CARE,
            stencilStoreOp=VK_ATTACHMENT_STORE_OP_DONT_CARE,
            initialLayout=VK_IMAGE_LAYOUT_UNDEFINED,
            finalLayout=VK_IMAGE_LAYOUT_PRESENT_SRC_KHR,
        )

        color_attachment_ref = VkAttachmentReference(
            attachment=0,
            layout=VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL,
        )

        subpass = VkSubpassDescription(
            pipelineBindPoint=VK_PIPELINE_BIND_POINT_GRAPHICS,
            colorAttachmentCount=1,
            pColorAttachments=[color_attachment_ref],
        )

        dependency = VkSubpassDependency(
            srcSubpass=VK_SUBPASS_EXTERNAL,
            dstSubpass=0,
            srcStageMask=VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,
            srcAccessMask=0,
            dstStageMask=VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT,
            dstAccessMask=VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT,
        )

        render_pass_info = VkRenderPassCreateInfo(
            sType=VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO,
            attachmentCount=1,
            pAttachments=[color_attachment],
            subpassCount=1,
            pSubpasses=[subpass],
            dependencyCount=1,
            pDependencies=[dependency],
        )

        self.render_pass = vkCreateRenderPass(self.device, render_pass_info, None)

    def _create_framebuffers(self):
        self.framebuffers = []

        for image_view in self.swapchain_image_views:
            fb_info = VkFramebufferCreateInfo(
                sType=VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO,
                renderPass=self.render_pass,
                attachmentCount=1,
                pAttachments=[image_view],
                width=self.swapchain_extent.width,
                height=self.swapchain_extent.height,
                layers=1,
            )
            self.framebuffers.append(vkCreateFramebuffer(self.device, fb_info, None))

    def _create_command_pool(self):
        pool_info = VkCommandPoolCreateInfo(
            sType=VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO,
            queueFamilyIndex=self._queue_family_indices["graphics"],
            flags=VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT,
        )
        self.command_pool = vkCreateCommandPool(self.device, pool_info, None)

    def _create_command_buffers(self):
        alloc_info = VkCommandBufferAllocateInfo(
            sType=VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO,
            commandPool=self.command_pool,
            level=VK_COMMAND_BUFFER_LEVEL_PRIMARY,
            commandBufferCount=len(self.swapchain_images),
        )
        self.command_buffers = vkAllocateCommandBuffers(self.device, alloc_info)

    def _record_command_buffer(self, command_buffer, image_index):
        begin_info = VkCommandBufferBeginInfo(sType=VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO)
        vkBeginCommandBuffer(command_buffer, begin_info)

        old_layout = VK_IMAGE_LAYOUT_PRESENT_SRC_KHR if self._image_initialized[image_index] else VK_IMAGE_LAYOUT_UNDEFINED

        to_transfer = VkImageMemoryBarrier(
            sType=VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER,
            oldLayout=old_layout,
            newLayout=VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
            srcQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,
            dstQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,
            image=self.swapchain_images[image_index],
            subresourceRange=VkImageSubresourceRange(
                aspectMask=VK_IMAGE_ASPECT_COLOR_BIT,
                baseMipLevel=0,
                levelCount=1,
                baseArrayLayer=0,
                layerCount=1,
            ),
            srcAccessMask=0,
            dstAccessMask=VK_ACCESS_TRANSFER_WRITE_BIT,
        )
        vkCmdPipelineBarrier(
            command_buffer,
            VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT if old_layout == VK_IMAGE_LAYOUT_UNDEFINED else VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT,
            VK_PIPELINE_STAGE_TRANSFER_BIT,
            0,
            0,
            None,
            0,
            None,
            1,
            [to_transfer],
        )

        copy_region = VkBufferImageCopy(
            bufferOffset=0,
            bufferRowLength=0,
            bufferImageHeight=0,
            imageSubresource=VkImageSubresourceLayers(
                aspectMask=VK_IMAGE_ASPECT_COLOR_BIT,
                mipLevel=0,
                baseArrayLayer=0,
                layerCount=1,
            ),
            imageOffset=VkOffset3D(x=0, y=0, z=0),
            imageExtent=VkExtent3D(width=self.swapchain_extent.width, height=self.swapchain_extent.height, depth=1),
        )
        vkCmdCopyBufferToImage(
            command_buffer,
            self._staging_buffer,
            self.swapchain_images[image_index],
            VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
            1,
            [copy_region],
        )

        to_present = VkImageMemoryBarrier(
            sType=VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER,
            oldLayout=VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
            newLayout=VK_IMAGE_LAYOUT_PRESENT_SRC_KHR,
            srcQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,
            dstQueueFamilyIndex=VK_QUEUE_FAMILY_IGNORED,
            image=self.swapchain_images[image_index],
            subresourceRange=VkImageSubresourceRange(
                aspectMask=VK_IMAGE_ASPECT_COLOR_BIT,
                baseMipLevel=0,
                levelCount=1,
                baseArrayLayer=0,
                layerCount=1,
            ),
            srcAccessMask=VK_ACCESS_TRANSFER_WRITE_BIT,
            dstAccessMask=0,
        )
        vkCmdPipelineBarrier(
            command_buffer,
            VK_PIPELINE_STAGE_TRANSFER_BIT,
            VK_PIPELINE_STAGE_BOTTOM_OF_PIPE_BIT,
            0,
            0,
            None,
            0,
            None,
            1,
            [to_present],
        )

        self._image_initialized[image_index] = True

        vkEndCommandBuffer(command_buffer)

    def _clear_cpu_framebuffer(self):
        r = max(0, min(255, int(self._color.r * 255)))
        g = max(0, min(255, int(self._color.g * 255)))
        b = max(0, min(255, int(self._color.b * 255)))
        a = max(0, min(255, int(self._color.a * 255)))
        if self._swapchain_is_bgra:
            self._cpu_framebuffer_np[:, :, 0] = b
            self._cpu_framebuffer_np[:, :, 1] = g
            self._cpu_framebuffer_np[:, :, 2] = r
            self._cpu_framebuffer_np[:, :, 3] = a
        else:
            self._cpu_framebuffer_np[:, :, 0] = r
            self._cpu_framebuffer_np[:, :, 1] = g
            self._cpu_framebuffer_np[:, :, 2] = b
            self._cpu_framebuffer_np[:, :, 3] = a

    def _blend_pixel(self, x, y, sr, sg, sb, sa):
        if x < 0 or y < 0 or x >= self._fb_width or y >= self._fb_height:
            return
        idx = (y * self._fb_width + x) * 4
        if self._swapchain_is_bgra:
            db = self._cpu_framebuffer[idx]
            dg = self._cpu_framebuffer[idx + 1]
            dr = self._cpu_framebuffer[idx + 2]
        else:
            dr = self._cpu_framebuffer[idx]
            dg = self._cpu_framebuffer[idx + 1]
            db = self._cpu_framebuffer[idx + 2]
        da = self._cpu_framebuffer[idx + 3]

        # Fast path for fully opaque source.
        if sa >= 255:
            if self._swapchain_is_bgra:
                self._cpu_framebuffer[idx] = sb
                self._cpu_framebuffer[idx + 1] = sg
                self._cpu_framebuffer[idx + 2] = sr
            else:
                self._cpu_framebuffer[idx] = sr
                self._cpu_framebuffer[idx + 1] = sg
                self._cpu_framebuffer[idx + 2] = sb
            self._cpu_framebuffer[idx + 3] = 255
            return

        inv = 255 - sa
        out_r = (sr * sa + dr * inv) // 255
        out_g = (sg * sa + dg * inv) // 255
        out_b = (sb * sa + db * inv) // 255
        out_a = sa + (da * inv) // 255

        if self._swapchain_is_bgra:
            self._cpu_framebuffer[idx] = out_b
            self._cpu_framebuffer[idx + 1] = out_g
            self._cpu_framebuffer[idx + 2] = out_r
        else:
            self._cpu_framebuffer[idx] = out_r
            self._cpu_framebuffer[idx + 1] = out_g
            self._cpu_framebuffer[idx + 2] = out_b
        self._cpu_framebuffer[idx + 3] = out_a

    def _draw_entity_axis_aligned(self, entity, texture_info, rot_flip):
        tw = int(texture_info["width"])
        th = int(texture_info["height"])
        if tw <= 0 or th <= 0:
            return

        tex = texture_info["pixels_np"]
        half_w = abs(float(entity.w) * float(entity.scale_x)) * 0.5
        half_h = abs(float(entity.h) * float(entity.scale_y)) * 0.5
        if half_w < 0.5 or half_h < 0.5:
            return

        sx0, sy0 = self._world_to_screen(float(entity.x) - half_w, float(entity.y) + half_h)
        sx1, sy1 = self._world_to_screen(float(entity.x) + half_w, float(entity.y) - half_h)

        left = int(math.floor(min(sx0, sx1)))
        right = int(math.ceil(max(sx0, sx1)))
        top = int(math.floor(min(sy0, sy1)))
        bottom = int(math.ceil(max(sy0, sy1)))

        min_x = max(0, left)
        max_x = min(self._fb_width - 1, right)
        min_y = max(0, top)
        max_y = min(self._fb_height - 1, bottom)
        if min_x > max_x or min_y > max_y:
            return

        color_r = max(0.0, min(1.0, float(entity.color.r)))
        color_g = max(0.0, min(1.0, float(entity.color.g)))
        color_b = max(0.0, min(1.0, float(entity.color.b)))
        color_a = max(0.0, min(1.0, float(entity.color.a)))

        flip_u = (float(entity.scale_x) < 0.0) ^ rot_flip
        flip_v = (float(entity.scale_y) < 0.0) ^ rot_flip

        xs = np.arange(min_x, max_x + 1, dtype=np.float32) + 0.5
        ys = np.arange(min_y, max_y + 1, dtype=np.float32) + 0.5

        ww = float(max(1, self.width))
        wh = float(max(1, self.height))
        fbw = float(max(1, self._fb_width))
        fbh = float(max(1, self._fb_height))

        wx = (xs / fbw) * ww - (ww * 0.5)
        wy = (wh * 0.5) - (ys / fbh) * wh

        camera = self._camera
        if camera is not None:
            zoom = float(camera.zoom)
            rot_rad = math.radians(float(camera.rotation))
            c = math.cos(rot_rad)
            s = math.sin(rot_rad)
            wx_raw = wx / max(1e-6, zoom)
            wy_raw = wy / max(1e-6, zoom)
            wx = wx_raw * c - wy_raw * s + float(camera.x)
            wy = wx_raw * s + wy_raw * c + float(camera.y)

        inv_w = 1.0 / max(1.0, (2.0 * half_w))
        inv_h = 1.0 / max(1.0, (2.0 * half_h))

        u = ((wx - float(entity.x)) * inv_w) + 0.5
        v = ((wy - float(entity.y)) * inv_h) + 0.5

        if flip_u:
            u = 1.0 - u
        if flip_v:
            v = 1.0 - v

        # Match OpenGL-style orientation from existing engine assets.
        v = 1.0 - v

        tx = np.clip((u * (tw - 1)).astype(np.int32), 0, tw - 1)
        ty = np.clip((v * (th - 1)).astype(np.int32), 0, th - 1)

        src = tex[ty[:, None], tx[None, :], :].astype(np.uint16)
        src[:, :, 0] = (src[:, :, 0] * int(color_r * 255)) // 255
        src[:, :, 1] = (src[:, :, 1] * int(color_g * 255)) // 255
        src[:, :, 2] = (src[:, :, 2] * int(color_b * 255)) // 255
        src[:, :, 3] = (src[:, :, 3] * int(color_a * 255)) // 255

        dst = self._cpu_framebuffer_np[min_y:max_y + 1, min_x:max_x + 1, :]
        dst16 = dst.astype(np.uint16)

        sa = src[:, :, 3]
        inv = 255 - sa

        if self._swapchain_is_bgra:
            dr = dst16[:, :, 2]
            dg = dst16[:, :, 1]
            db = dst16[:, :, 0]
        else:
            dr = dst16[:, :, 0]
            dg = dst16[:, :, 1]
            db = dst16[:, :, 2]
        da = dst16[:, :, 3]

        out_r = (src[:, :, 0] * sa + dr * inv) // 255
        out_g = (src[:, :, 1] * sa + dg * inv) // 255
        out_b = (src[:, :, 2] * sa + db * inv) // 255
        out_a = sa + (da * inv) // 255

        if self._swapchain_is_bgra:
            dst[:, :, 0] = np.clip(out_b, 0, 255).astype(np.uint8)
            dst[:, :, 1] = np.clip(out_g, 0, 255).astype(np.uint8)
            dst[:, :, 2] = np.clip(out_r, 0, 255).astype(np.uint8)
        else:
            dst[:, :, 0] = np.clip(out_r, 0, 255).astype(np.uint8)
            dst[:, :, 1] = np.clip(out_g, 0, 255).astype(np.uint8)
            dst[:, :, 2] = np.clip(out_b, 0, 255).astype(np.uint8)
        dst[:, :, 3] = np.clip(out_a, 0, 255).astype(np.uint8)

    def _world_to_screen(self, x, y):
        ww = float(max(1, self.width))
        wh = float(max(1, self.height))
        camera = self._camera
        if camera is not None:
            rot_rad = math.radians(float(camera.rotation))
            zoom = float(camera.zoom)
            dx = float(x) - float(camera.x)
            dy = float(y) - float(camera.y)
            c = math.cos(-rot_rad)
            s = math.sin(-rot_rad)
            tx = dx * c - dy * s
            ty = dx * s + dy * c
            tx *= zoom
            ty *= zoom
        else:
            tx = float(x)
            ty = float(y)
        sx = ((tx + (ww * 0.5)) / ww) * float(self._fb_width)
        sy = (((wh * 0.5) - ty) / wh) * float(self._fb_height)
        return sx, sy

    def _screen_to_world(self, sx, sy):
        ww = float(max(1, self.width))
        wh = float(max(1, self.height))
        tx = (float(sx) / float(max(1, self._fb_width))) * ww - (ww * 0.5)
        ty = (wh * 0.5) - ((float(sy) / float(max(1, self._fb_height))) * wh)
        camera = self._camera
        if camera is not None:
            rot_rad = math.radians(float(camera.rotation))
            zoom = float(camera.zoom)
            tx /= max(1e-6, zoom)
            ty /= max(1e-6, zoom)
            c = math.cos(rot_rad)
            s = math.sin(rot_rad)
            wx = tx * c - ty * s + float(camera.x)
            wy = tx * s + ty * c + float(camera.y)
        else:
            wx = tx
            wy = ty
        return wx, wy

    def _screen_to_world_x(self, sx):
        ww = float(max(1, self.width))
        tx = (float(sx) / float(max(1, self._fb_width))) * ww - (ww * 0.5)
        camera = self._camera
        if camera is not None:
            tx /= max(1e-6, float(camera.zoom))
            tx += float(camera.x)
        return tx

    def _screen_to_world_y(self, sy):
        wh = float(max(1, self.height))
        ty = (wh * 0.5) - ((float(sy) / float(max(1, self._fb_height))) * wh)
        camera = self._camera
        if camera is not None:
            ty /= max(1e-6, float(camera.zoom))
            ty += float(camera.y)
        return ty

    def _draw_entity_software(self, entity):
        texture_info = self._textures.get(getattr(entity.texture, "id", None))
        if not texture_info:
            return

        rot = float(entity.rotation) % 360.0
        if abs(rot) < 0.001:
            self._draw_entity_axis_aligned(entity, texture_info, rot_flip=False)
            return
        if abs(rot - 180.0) < 0.001:
            self._draw_entity_axis_aligned(entity, texture_info, rot_flip=True)
            return

        tw = int(texture_info["width"])
        th = int(texture_info["height"])
        if tw <= 0 or th <= 0:
            return

        tex = texture_info["pixels_np"]

        half_w = abs(float(entity.w) * float(entity.scale_x)) * 0.5
        half_h = abs(float(entity.h) * float(entity.scale_y)) * 0.5
        if half_w < 0.5 or half_h < 0.5:
            return

        angle = math.radians(float(entity.rotation))
        ca = math.cos(angle)
        sa = math.sin(angle)

        corners = [(-half_w, -half_h), (half_w, -half_h), (half_w, half_h), (-half_w, half_h)]
        screen_pts = []
        for lx, ly in corners:
            wx = float(entity.x) + lx * ca - ly * sa
            wy = float(entity.y) + lx * sa + ly * ca
            sx, sy = self._world_to_screen(wx, wy)
            screen_pts.append((sx, sy))

        min_x = max(0, int(math.floor(min(p[0] for p in screen_pts))))
        max_x = min(self._fb_width - 1, int(math.ceil(max(p[0] for p in screen_pts))))
        min_y = max(0, int(math.floor(min(p[1] for p in screen_pts))))
        max_y = min(self._fb_height - 1, int(math.ceil(max(p[1] for p in screen_pts))))
        if min_x > max_x or min_y > max_y:
            return

        inv_ca = math.cos(-angle)
        inv_sa = math.sin(-angle)

        color_r = max(0.0, min(1.0, float(entity.color.r)))
        color_g = max(0.0, min(1.0, float(entity.color.g)))
        color_b = max(0.0, min(1.0, float(entity.color.b)))
        color_a = max(0.0, min(1.0, float(entity.color.a)))

        flip_u = float(entity.scale_x) < 0.0
        flip_v = float(entity.scale_y) < 0.0

        for py in range(min_y, max_y + 1):
            for px in range(min_x, max_x + 1):
                wx, wy = self._screen_to_world(px + 0.5, py + 0.5)

                dx = wx - float(entity.x)
                dy = wy - float(entity.y)

                lx = dx * inv_ca - dy * inv_sa
                ly = dx * inv_sa + dy * inv_ca

                if abs(lx) > half_w or abs(ly) > half_h:
                    continue

                u = (lx / (2.0 * half_w)) + 0.5
                v = (ly / (2.0 * half_h)) + 0.5
                if flip_u:
                    u = 1.0 - u
                if flip_v:
                    v = 1.0 - v

                # Match OpenGL-style orientation from existing engine assets.
                v = 1.0 - v

                tx = max(0, min(tw - 1, int(u * (tw - 1))))
                ty = max(0, min(th - 1, int(v * (th - 1))))

                tr, tg, tb, ta = tex[ty, tx]

                sr = int(tr * color_r)
                sg = int(tg * color_g)
                sb = int(tb * color_b)
                sa_px = int(ta * color_a)
                if sa_px <= 0:
                    continue

                self._blend_pixel(px, py, sr, sg, sb, sa_px)

    def _rasterize_entities_to_cpu(self):
        self._clear_cpu_framebuffer()
        if not self._pending_entities:
            return
        for entity in self._pending_entities:
            self._draw_entity_software(entity)

    def _upload_cpu_framebuffer(self):
        mapped = vkMapMemory(self.device, self._staging_memory, 0, self._fb_size, 0)
        if isinstance(mapped, tuple):
            mapped = mapped[-1]

        src = ffi.from_buffer(self._cpu_framebuffer)
        try:
            ffi.memmove(mapped, src, self._fb_size)
        except TypeError:
            addr = None
            try:
                addr = int(mapped)
            except Exception:
                if hasattr(mapped, "value"):
                    try:
                        addr = int(mapped.value)
                    except Exception:
                        addr = None
            if addr is None:
                raise RuntimeError(f"Unsupported vkMapMemory pointer type: {type(mapped)}")
            ffi.memmove(addr, src, self._fb_size)

        vkUnmapMemory(self.device, self._staging_memory)

    def _create_sync_objects(self):
        sem_info = VkSemaphoreCreateInfo(sType=VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO)
        fence_info = VkFenceCreateInfo(
            sType=VK_STRUCTURE_TYPE_FENCE_CREATE_INFO,
            flags=VK_FENCE_CREATE_SIGNALED_BIT,
        )

        self.image_available_semaphores = []
        self.render_finished_semaphores = []
        self.in_flight_fences = []

        for _ in range(self._max_frames_in_flight):
            self.image_available_semaphores.append(vkCreateSemaphore(self.device, sem_info, None))
            self.render_finished_semaphores.append(vkCreateSemaphore(self.device, sem_info, None))
            self.in_flight_fences.append(vkCreateFence(self.device, fence_info, None))

    # Rendering
    def _draw_frame(self):
        wait_result = vkWaitForFences(
            self.device,
            1,
            [self.in_flight_fences[self._current_frame]],
            True,
            self._fence_wait_timeout_ns,
        )
        wait_result = self._parse_result_code(wait_result)
        if wait_result == VK_TIMEOUT:
            logLn("Vulkan fence wait timed out, attempting renderer recovery.", "error logger")
            self._recover_vulkan_renderer()
            return
        if wait_result not in (VK_SUCCESS,):
            raise RuntimeError(f"vkWaitForFences failed with result={wait_result}")

        image_index_ptr = ffi.new("uint32_t[1]")
        try:
            acquire_result = self.vkAcquireNextImageKHR(
                self.device,
                self.swapchain,
                0xFFFFFFFFFFFFFFFF,
                self.image_available_semaphores[self._current_frame],
                VK_NULL_HANDLE,
                image_index_ptr,
            )
        except VkErrorOutOfDateKhr:
            self._recreate_swapchain()
            return

        acquire_result = self._parse_result_code(acquire_result)
        if acquire_result == VK_ERROR_OUT_OF_DATE_KHR:
            self._recreate_swapchain()
            return
        if acquire_result not in (VK_SUCCESS, VK_SUBOPTIMAL_KHR):
            raise RuntimeError(f"vkAcquireNextImageKHR failed with result={acquire_result}")

        image_index = int(image_index_ptr[0])
        if image_index < 0 or image_index >= len(self.command_buffers):
            raise RuntimeError(f"Acquire returned invalid image index {image_index} for {len(self.command_buffers)} command buffers")

        if self._framebuffer_resized:
            self._framebuffer_resized = False
            self._recreate_swapchain()
            return

        self._rasterize_entities_to_cpu()
        self._upload_cpu_framebuffer()

        vkResetFences(self.device, 1, [self.in_flight_fences[self._current_frame]])
        vkResetCommandBuffer(self.command_buffers[image_index], 0)
        self._record_command_buffer(self.command_buffers[image_index], image_index)

        submit_info = VkSubmitInfo(
            sType=VK_STRUCTURE_TYPE_SUBMIT_INFO,
            waitSemaphoreCount=1,
            pWaitSemaphores=[self.image_available_semaphores[self._current_frame]],
            pWaitDstStageMask=[VK_PIPELINE_STAGE_TRANSFER_BIT],
            commandBufferCount=1,
            pCommandBuffers=[self.command_buffers[image_index]],
            signalSemaphoreCount=1,
            pSignalSemaphores=[self.render_finished_semaphores[self._current_frame]],
        )

        vkQueueSubmit(self.graphics_queue, 1, [submit_info], self.in_flight_fences[self._current_frame])

        present_info = VkPresentInfoKHR(
            sType=VK_STRUCTURE_TYPE_PRESENT_INFO_KHR,
            waitSemaphoreCount=1,
            pWaitSemaphores=[self.render_finished_semaphores[self._current_frame]],
            swapchainCount=1,
            pSwapchains=[self.swapchain],
            pImageIndices=[image_index],
        )

        try:
            present_result = self.vkQueuePresentKHR(self.present_queue, present_info)
            present_result = self._parse_result_code(present_result)
            if present_result == VK_ERROR_OUT_OF_DATE_KHR:
                self._recreate_swapchain()
        except VkErrorOutOfDateKhr:
            self._recreate_swapchain()

        self._current_frame = (self._current_frame + 1) % self._max_frames_in_flight

    def _parse_result_code(self, value):
        known = {VK_SUCCESS, VK_SUBOPTIMAL_KHR, VK_ERROR_OUT_OF_DATE_KHR, VK_TIMEOUT}
        if isinstance(value, tuple):
            for item in value:
                try:
                    item_i = int(item)
                except Exception:
                    continue
                if item_i in known:
                    return item_i
            return VK_SUCCESS
        try:
            value_i = int(value)
            if value_i in known:
                return value_i
        except Exception:
            pass
        return VK_SUCCESS

    def _recreate_swapchain(self):
        w, h = glfw.get_framebuffer_size(self.handle)
        while w == 0 or h == 0:
            glfw.wait_events()
            w, h = glfw.get_framebuffer_size(self.handle)

        vkDeviceWaitIdle(self.device)

        if getattr(self, "command_buffers", None):
            vkFreeCommandBuffers(self.device, self.command_pool, len(self.command_buffers), self.command_buffers)
            self.command_buffers = []

        self._destroy_software_framebuffer_resources()
        self.vkDestroySwapchainKHR(self.device, self.swapchain, None)

        self._create_swapchain_and_dependents()
        self._create_software_framebuffer_resources()
        self._create_command_buffers()

    def _destroy_vulkan_objects_best_effort(self):
        # Device can already be lost; every destroy call here is best-effort.
        device = getattr(self, "device", None)
        if device is not None:
            try:
                vkDeviceWaitIdle(device)
            except Exception:
                pass

        sems = getattr(self, "image_available_semaphores", [])
        fins = getattr(self, "render_finished_semaphores", [])
        fences = getattr(self, "in_flight_fences", [])
        for i in range(min(len(sems), len(fins), len(fences))):
            try:
                vkDestroySemaphore(device, sems[i], None)
            except Exception:
                pass
            try:
                vkDestroySemaphore(device, fins[i], None)
            except Exception:
                pass
            try:
                vkDestroyFence(device, fences[i], None)
            except Exception:
                pass

        self.image_available_semaphores = []
        self.render_finished_semaphores = []
        self.in_flight_fences = []

        try:
            self._destroy_software_framebuffer_resources()
        except Exception:
            pass

        if device is not None and getattr(self, "command_pool", None):
            try:
                vkDestroyCommandPool(device, self.command_pool, None)
            except Exception:
                pass
            self.command_pool = None

        if device is not None and getattr(self, "swapchain", None):
            try:
                self.vkDestroySwapchainKHR(device, self.swapchain, None)
            except Exception:
                pass
            self.swapchain = None

        if device is not None:
            try:
                vkDestroyDevice(device, None)
            except Exception:
                pass
            self.device = None

        if getattr(self, "surface", None):
            try:
                self.vkDestroySurfaceKHR(self.instance, self.surface, None)
            except Exception:
                pass
            self.surface = None

        if getattr(self, "instance", None):
            try:
                vkDestroyInstance(self.instance, None)
            except Exception:
                pass
            self.instance = None

    def _recover_vulkan_renderer(self):
        if self._recovering:
            return
        self._recovering = True
        try:
            self._destroy_vulkan_objects_best_effort()
            self._create_vulkan_context()
            self._current_frame = 0
            logLn("Vulkan renderer recovered.")
        except Exception as exc:
            logLn(f"Vulkan recovery failed: {exc}", "error logger")
            glfw.set_window_should_close(self.handle, True)
        finally:
            self._recovering = False

    # Cleanup
    def _cleanup(self):
        if getattr(self, "device", None) is None:
            return

        vkDeviceWaitIdle(self.device)

        for i in range(len(self.image_available_semaphores)):
            vkDestroySemaphore(self.device, self.image_available_semaphores[i], None)
            vkDestroySemaphore(self.device, self.render_finished_semaphores[i], None)
            vkDestroyFence(self.device, self.in_flight_fences[i], None)

        self._destroy_software_framebuffer_resources()

        if getattr(self, "command_pool", None):
            vkDestroyCommandPool(self.device, self.command_pool, None)

        if getattr(self, "swapchain", None):
            self.vkDestroySwapchainKHR(self.device, self.swapchain, None)

        if getattr(self, "device", None):
            vkDestroyDevice(self.device, None)

        if getattr(self, "surface", None):
            self.vkDestroySurfaceKHR(self.instance, self.surface, None)

        if getattr(self, "instance", None):
            vkDestroyInstance(self.instance, None)