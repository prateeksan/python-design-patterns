""" The Facade Pattern

Notes:

In my opinion, this is one of the most intuitive design patterns that I have
come across. The point of the Facade pattern is to create a high-level unified
interface that hides more complex objects behind it. It is particularly useful
in situations where:

> There is need for a system which relies on complex sub-systems or sub-objects.
> The user of this system needs to a see a simple interface.
> The system can be represented as an object.

In the following example, the Dashboard class represents a facade for a complex
set of sub-systems - APIs of different teams within an organization. In this
case, the user of the dashboard is interested only in getting aggregated
performance reports from campaign teams and updating their budgets with
allocation adjustments. The facade thus exposes only two simple methods while
hiding all other internal interactions.

"""

class AbstractCampaignApi():
    """Acts as an abstract parent, defining the interface of campaign
    APIs. In a real use case, it may be worthwhile to force the implementation
    of some or all methods declared here."""

    def get_performance_report(self):
        pass
    def get_spend_report(self):
        pass
    def update_budget(self, budget):
        pass

class VideoCampaignApi(AbstractCampaignApi):
    """Connects to the API of the hypothetical video campaigns team."""
    pass

class RadioCampaignApi(AbstractCampaignApi):
    """Connects to the API of the hypothetical radio campaigns team."""
    pass

class AccountsApi():
    """Connects to the API of the hypothetical accounts team. Note how the
    interface is different from campaign APIs - a complexity that will be hidden
    by the facade.
    """

    def report_spending(self, medium, spending):
        pass
    def get_new_budget(self, medium, weight):
        pass

class Dashboard():
    """This class acts as the facade to hide all the complex interactions
    between the APIs of different company teams."""

    def __init__(self, user, token):
        """Instantiating the facade automatically handles authentication and 
        connections to all relevant APIs (logic for this would go in the API
        wrapper classes in a real implementation."""

        self._authenticate(user, token)
        self.campaign_apis = {
            "video": VideoCampaignApi(), 
            "radio": RadioCampaignApi()
        }
        self.accounts_api = AccountsApi()

    def full_performance_report(self):
        """Provides the user of the dashboard a simple interface to aggregate
        performance data from all campaign teams."""

        reports = []
        for medium in self.campaign_apis:
            print("Getting {} performance report...".format(medium))
            reports.append(self.campaign_apis[medium].get_performance_report())

        print("Compiling aggregate report...")
        compiled_report = self._agg_campaign_performance_report(reports)

        print("Done!" + "\n")
        return self._agg_campaign_performance_report(reports)

    def update_budget(self, medium, weight):
        """Once again provides a simple interface to perform the complex task of
        updating a campaign team's budget. We assume that the user will specify
        a 'weight' that may affect the budget allocation."""

        print("Updating budget for {} campaigns...".format(medium))

        print("Generating spendings report...")
        spend_report = self.campaign_apis[medium].get_spend_report()

        print("Sending spendings report to the accounts team...")
        self.accounts_api.report_spending(medium=medium, spending=spend_report)

        print("Generating new budget with weight recalculations...")
        new_budget = self.accounts_api.get_new_budget(medium=medium, 
            weight=weight)

        print("Sending new budget to the campaigns team...")
        self.campaign_apis[medium].update_budget(new_budget)

        print("Done!" + "\n")

    def _authenticate(self, user, token):
        """Private method that the user need not deal with directly."""
        pass

    def _agg_campaign_performance_report(self, reports):
        """Private method that the user need not deal with directly."""
        pass


if __name__ == "__main__":

    user = "sample.manager@samplecompany.com"
    token = "xxxxxx"

    dashboard = Dashboard(user, token)
    # Aggregated report that the user can use at their discretion.
    dashboard.full_performance_report()
    # Budgetary re-sallocations (that may be made after reviewing the report).
    dashboard.update_budget("video", 0.8)
    dashboard.update_budget("radio", 0.2)
