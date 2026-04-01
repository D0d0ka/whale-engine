from .engine import current_app

def destroy(entity):
    if entity.entity_type == "Entity":
        if entity in entity.renderer.entities:
            entity.renderer.entities.remove(entity)
        for i in list(entity.parentings):
            destroy(i)
    elif entity.entity_type == "Circle Collider":
        if entity.visualize:
            destroy(entity.visualition)
        for i in list(entity.parentings):
            destroy(i)
        if entity in current_app.CircleCollisionSystem2D.circle_colliders:
            current_app.CircleCollisionSystem2D.circle_colliders.remove(entity)
    elif entity.entity_type == "Parenting":
        if entity in current_app.ParentingSystem.parentchildrelationships:
            current_app.ParentingSystem.parentchildrelationships.remove(entity)
    elif entity.entity_type in ["Mesh circle Collider", "Mesh Better Collider", "Mesh Collider"]:
        if hasattr(entity, "dots"):
            for dot in entity.dots:
                destroy(dot)
        for i in list(entity.parentings):
            destroy(i)
        if hasattr(current_app, "CircleCollisionSystem2D") and entity in current_app.CircleCollisionSystem2D.mesh_colliders:
            current_app.CircleCollisionSystem2D.mesh_colliders.remove(entity)
        if hasattr(current_app, "BetterCollisionSystem2D") and entity in current_app.BetterCollisionSystem2D.colliders:
            current_app.BetterCollisionSystem2D.colliders.remove(entity)
    elif entity.entity_type == "Quad Collider":
        if entity.visualize:
            destroy(entity.visualition)
        for i in list(entity.parentings):
            destroy(i)
        if hasattr(current_app, "BetterCollisionSystem") and entity in current_app.BetterCollisionSystem2D.colliders:
            current_app.BetterCollisionSystem2D.colliders.remove(entity)
    elif entity.entity_type == "Line":
        for part in entity.parts:
            destroy(part)
        destroy(entity.start)
        destroy(entity.end)
    else:
        raise ValueError(f"Unknown entity type: {entity.entity_type}")