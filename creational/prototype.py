""" The Prototye Pattern

Notes:

In the prototype pattern, rather than creating new instances of an object, only
one instance (the breeder) of a class (the prototype) is created and deep-copied
whenever the need arises. This pattern is particularly useful when:

+ The cost of initialization is high.
+ Many objects of the same type are needed but some (or all) properties that are
    costly (time/space/bandwidth) to set remain the same across all objects.

The following example considers the use case of a prototype for student report
cards. Let us assume that all report cards for any given year have some universal
data that might take a long time to query and post-process. Let us also assume
that each report card belongs to a student and contains some data that is unique
to the student and can be populated after the universal data has been populated.
This is a good use case for the pattern since we only need one instance of the
ReportCardPrototype per year (the breeder for that year). To create report
card(s) for a particular student, we only need to make one clone of each breeder
associated to the year that the student was enrolled.

"""

import copy

class ReportCardPrototype:
    """The prototype class for report cards."""

    def __init__(self, year):
        """Only one instance per year should be constructed."""

        self.year = year
        self.report = None
        self.student_id = None
        self._build_general_report()

    def set_student(self, s_id):
        """Updates the report data with student specific data. Only clones of
        the breeders should call this.
        """

        self.student_id = s_id
        self._populate_student_data()

    def _build_general_report(self):
        """We assume that this method is very costly. The point of the pattern 
        to call it as rarely as possible.
        """
        pass

    def _populate_student_data(self):
        """This populates the student data and should only be called by
        set_student. All costly computations and queries per clone should be
        contained here.
        """
        pass

    def clone(self):
        """Any clone of the breeders should be made by calling this method."""

        # The copy created is a brand new object with its own id and properties.
        return copy.deepcopy(self)

    def __repr__(self):

        return "<ReportCard: student_id: {}, year: {}>".format(self.student_id,
            self.year)

class ReportFactory():
    """This is not strictly a part of the prototype pattern but complements it
    very well. All instances of the prototype (breeders) are contained in this
    class. They can then be interfaced with using the `make()` method. It may
    be implemented differently (as a singleton or with a caching model).
    """

    _report_breeders = {}
    
    def __init__(self):
        """Further implementation may be added here as per your use case."""
        pass

    def make(self, s_id, year):
        """Similar to any factory, this method adds a layer of abstraction to
        the object creation. In this case, it ensures that the right breeder is
        cloned.
        """

        if year not in ReportFactory._report_breeders:
            ReportFactory._report_breeders[year] = ReportCardPrototype(year)

        clone = ReportFactory._report_breeders[year].clone()
        clone.set_student(s_id)
        return clone

class Student():
    """This class is not pertinent to the prototype pattern but it adds some
    elegenace to this example. Simply by instantiating a Student, all its
    report cards for all years are automatically generated.
    """

    def __init__(self, s_id, years, report_factory):

        self.id = s_id
        self.years = years
        self.report_cards = []
        self.report_factory = report_factory
        self._get_report_cards()

    def _get_report_cards(self):

        for year in self.years:
            report_card = self.report_factory.make(self.id, year)
            self.report_cards.append(report_card)


if __name__ == "__main__":

    # The factory acts as an interface to prototype breeders.
    factory = ReportFactory()
    # Constructing a student automatically clones all breeders for his/her years.
    student_1234 = Student(s_id=1234, years=[2015, 2016], report_factory=factory)
    student_4321 = Student(s_id=4321, years=[2014, 2015], report_factory=factory)

    print(student_1234.report_cards)
    print(student_4321.report_cards)  
