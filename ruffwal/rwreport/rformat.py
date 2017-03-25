from geraldo import Report, ReportBand, ObjectValue, landscape

class DecimalObjectValue(ObjectValue):
    format = '%0.02f'
    def get_object_value(self, instance=None):
        value = super(DecimalObjectValue, self).get_object_value(instance)

        if not value:
            value = 0

        return self.format%value
