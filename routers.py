
class SaswatCustAppRouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'saswat_cust_app':
            return 'default'  # Use db2 for app1

        return None

    def db_for_write(self, model, **hints):

        if model._meta.app_label == 'saswat_cust_app':
            return 'default'

        return None

    def allow_relation(self, obj1, obj2, **hints):

        if obj1._meta.app_label == 'saswat_cust_app' and obj2._meta.app_label == 'saswat_cust_app':
            return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label == 'saswat_cust_app':
            return db == 'default'

        return None


class DataEntryAppRouter:

    def db_for_read(self, model, **hints):

        if model._meta.app_label == 'data_entry_app':
            return 'sqlit'  # Use default database for app2

        return None

    def db_for_write(self, model, **hints):

        if model._meta.app_label == 'data_entry_app':
            return 'sqlit'

        return None

    def allow_relation(self, obj1, obj2, **hints):

        if obj1._meta.app_label == 'data_entry_app' and obj2._meta.app_label == 'data_entry_app':
            return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label == 'data_entry_app':
            return db == 'sqlit'

        return None
