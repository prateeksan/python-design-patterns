""" The Command Pattern

Notes:

The command pattern encapsulates a series of commands into an object (the
Invoker). This allows the user to execute the commands in a preset order at a
later time. It also allows the Invoker to encapsulate additional behaviour (such
as the ability to handle a command's failure).

This example simulates a database migration system wherein a series of migration
commands need to be run atomically (all go through or none do) and in a specific
order. In this case, each command is encapsulated as an instance of
MigrationCommand (or its child), with the ability to run or rollback the
migration. The invoker is responsible for maintaining the sequence of migrations
and their atomicity by rolling back all completed migrations in case of a
failure. The invoker thus creates and handles a loose coupling of the 
migration commands.

"""

class MigrationCommand:
    """Represents a migration command which the invoker will call."""

    def __init__(self, title, instructions):
        self.title = title
        self.instructions = instructions

    def run(self):
        print("[i] Running Migration: {}".format(self.title))

    def rollback(self):
        print("[i] Rolling Back Migration: {}".format(self.title))

class BadMigrationCommand(MigrationCommand):
    """Created for demonstrative purposes only (to test a failure)."""

    def run(self): raise RuntimeError("Something went wrong.")

class Invoker:
    """Responsible for maintaining the sequence and atomicity of loosely coupled
    migration commands."""

    def __init__(self, migrations):

        self.migrations = migrations
        # Tracking the version allows the invoker to perform atomic rollbacks.
        self._version = 0

    def run_all(self):
        """Runs all migrations. If any fail, rolls back all migrations."""

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



