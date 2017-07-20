""" The Command Pattern

Notes:


"""

class MigrationCommand:

    def __init__(self, title, instructions):
        self.title = title
        self.instructions = instructions

    def run(self):
        print("[i] Running Migration: {}".format(self.title))

    def rollback(self):
        print("[i] Rolling Back Migration: {}".format(self.title))

class BadMigrationCommand(MigrationCommand):

    def run(self): raise RuntimeError("Something went wrong.")

class Invoker:

    def __init__(self, migrations):

        self.migrations = migrations
        self._version = 0

    def run_all(self):
        for migration in self.migrations:
            try:
                migration.run()
                self._version += 1
            except Exception as e:
                print("[!] Migrations failed due to a {}. Rolling back.".format(
                    e.__class__.__name__))
                self.rollback_all()
                return False
                # raise e

        print("[i] Migrations complete. Current Version: {}".format(
            self._version))

    def rollback_all(self):

        if self._version == 0:
            print("Nothing to rollback")
            return None

        for migration in reversed(self.migrations[:self._version]):
            migration.rollback()
            self._version -= 1

        print("[i] Rollbacks complete. Current Version: {}".format(
            self._version))

if __name__ == "__main__":

    migrations = [
        MigrationCommand(title="Create Table A", instructions={}),
        MigrationCommand(title="Create Table B", instructions={}),
        MigrationCommand(title="Create Associative Table AB", instructions={}),
        BadMigrationCommand(title="Do Something Impossible", instructions={}),
    ]

    print("Attempting to run a migration set with a bad migration:\n")
    migrations_invoker = Invoker(migrations)
    migrations_invoker.run_all()

    print("\n")

    print("Attempting to run the set with only valid migrations:\n")
    del migrations_invoker.migrations[-1]
    migrations_invoker.run_all()



