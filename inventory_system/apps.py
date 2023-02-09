from django.apps import AppConfig


class InventorySystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory_system'

    def ready(self):
        import inventory_system.notifications