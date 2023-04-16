Title: Generating XLSX (or CSV) from the Django admin (or elsewhere)
Slug: generating-xlsx-or-csv-from-the-django-admin-or-elsewhere
Date: 2022-08-17
Categories: Django, Programming

# Generating XLSX (or CSV) from the Django admin (or elsewhere)

The blog post [Django: excel output instead of csv](https://reinout.vanrees.org/weblog/2022/08/15/excel-instead-of-csv.html) inspired me to write about my own experience with XLSX or CSV generation.

## XLSX export

For a long time I used similarly structured ad-hoc code built on [xlwt](https://pypi.org/project/xlwt/), a project which looks abandoned these days. I have been a more or less happy user of [openpyxl](https://pypi.org/project/openpyxl/) during the last years and intend to continue using it.

Something which I (or rather my users) require often is a way to export a list of selected objects from the Django admin. A good way to achieve this is by using an [admin action](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/actions/). The common use case is that I have to export all model fields and maybe some additional data. [xlsxdocument](https://github.com/matthiask/xlsxdocument/) makes this very easy, all you have to do is:

    from django.contrib import admin
    from xlsxdocument import export_selected
    from app import models

    @admin.register(models.Example)
    class ExampleAdmin(admin.ModelAdmin):
        actions = [export_selected]

If you wanted more control and wanted to add an additional field at the end you could write your own view (or embed the code in your own action, see the Django docs for this):

    from xlsxdocument import export_selected
    from app.models import Example

    def generate_xlsx(request):
        xlsx = XLSXDocument()
        xlsx.table_from_queryset(
        	Example.objects.all(),
            additional=[
        		("URL", lambda obj: request.build_absolute_uri(obj.get_absolute_url())),
        	],
        )
        return xlsx.to_response("example.xlsx")

Or, you could go even lower and use `xlsx.add_sheet()` and `xlsx.table()` yourself.

Dates, datetimes, numbers, choice fields and Django model instances are (I hope!) handled in a good way automatically.

## CSV export for large datasets

For large datasets the xlsxdocument/openpyxl combination has proven to be too slow. I didn't take the time to profile things to find where all the time is spent. Instead, I stumbled over a very relevant section in the Django documentation: [Streaming large CSV files](https://docs.djangoproject.com/en/4.1/howto/outputting-csv/#streaming-large-csv-files) The code in there proved to be at least an order of magnitude faster (exports which produced server timeouts each time finished in a fraction of a second)

But, since I didn't want to go back to copy-pasting code and since I also didn't want to lose the automatic queryset handling I just had to write another library 😅 The result of this work is [django-fast-export](https://github.com/matthiask/django-fast-export/). Replicating the example from above (with the additional benefit of using a streaming response instead of building everything up-front) would look like this:

    from django_fast_export import StreamingCSVResponse, all_values, all_verbose_names
    from app.models import Example

    def generate_csv(request):
    	def _gen():
        	queryset = Example.objects.all()
        	yield (all_verbose_names(Example) + ["URL"])
            yield from (
                (all_values(instance) + [request.build_absolute_uri(instance.get_absolute_url())])
                for instance in queryset
    		)

        return StreamingCSVResponse(_gen())

## Links

- [xlsxdocument](https://github.com/matthiask/xlsxdocument/)
- [django-fast-export](https://github.com/matthiask/django-fast-export/)
