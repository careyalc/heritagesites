from django.db import models
from django.urls import reverse


class CountryArea(models.Model):
    country_area_id = models.AutoField(primary_key=True)
    country_area_name = models.CharField(unique=True, max_length=100)
  
    m49_code = models.SmallIntegerField()
    iso_alpha3_code = models.CharField(max_length=3)
    dev_status = models.ForeignKey('DevStatus', on_delete=models.PROTECT, blank=True, null=True)
    location = models.ForeignKey('Location', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country_area'
        ordering = ['country_area_name']
        verbose_name = 'UNSD M49 Country or Area'
        verbose_name_plural = 'UNSD M49 Countries or Areas'

    def __str__(self):
        return self.country_area_name


'''   
class CountryArea(models.Model):
    country_area_id = models.AutoField(primary_key=True)
    country_area_name = models.CharField(unique=True, max_length=100)
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)
    sub_region = models.ForeignKey('SubRegion', models.DO_NOTHING, blank=True, null=True)
    intermediate_region = models.ForeignKey('IntermediateRegion', models.DO_NOTHING, blank=True, null=True)
    m49_code = models.SmallIntegerField()
    iso_alpha3_code = models.CharField(max_length=3)
    dev_status = models.ForeignKey('DevStatus', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'country_area'
'''


class DevStatus(models.Model):
    dev_status_id = models.AutoField(primary_key=True)
    dev_status_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'dev_status'
        ordering = ['dev_status_name']
        verbose_name = 'UNSD M49 Country or Area Development Status'
        verbose_name_plural = 'UNSD M49 Country or Area Development Statuses'

    def __str__(self):
        return self.dev_status_name



class HeritageSite(models.Model):
    heritage_site_id = models.AutoField(primary_key=True)
    site_name = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    justification = models.TextField(blank=True, null=True)
    # date_inscribed = models.TextField(blank=True, null=True)  # This field type is a guess.
    date_inscribed = models.IntegerField(blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    area_hectares = models.FloatField(blank=True, null=True)
    heritage_site_category = models.ForeignKey('HeritageSiteCategory', on_delete=models.PROTECT)
    transboundary = models.IntegerField()

    # Intermediate model (country_area -> heritage_site_jurisdiction <- heritage_site)
    country_area = models.ManyToManyField(CountryArea, through='HeritageSiteJurisdiction')

    class Meta:
        managed = False
        db_table = 'heritage_site'
        ordering = ['site_name']
        verbose_name = 'UNESCO Heritage Site'
        verbose_name_plural = 'UNESCO Heritage Sites'

    def __str__(self):
        return self.site_name

    def country_area_display(self):
        """Create a string for country_area. This is required to display in the Admin view."""
        return ', '.join(
            country_area.country_area_name for country_area in self.country_area.all()[:25])

    country_area_display.short_description = 'Country or Area'

    def get_absolute_url(self):
        # return reverse('site_detail', args=[str(self.id)])
        return reverse('site_detail', kwargs={'pk': self.pk})

    ####ADD DECORATORS - see images from class ... but don;t worry about sort order for property? (ignore other param and if statement in photo)
    ### these decorators will replace "spagetti code" in the template - only use self as an arguement
    ##each one we have to write will be similar to the example - construct query set, create loop, and spit stuff out
    ####NOTE that he calls it country_area and mine is callsed omsoen else.......... 
    @property
    def country_area_names(self):
        """
        Returns a list of UNSD countries/areas (names only) associated with a Heritage Site.
        Note that not all Heritage Sites are associated with a country/area (e.g., Old City
        Walls of Jerusalem). In such cases the Queryset will return as <QuerySet [None]> and the
        list will need to be checked for None or a TypeError (sequence item 0: expected str
        instance, NoneType found) runtime error will be thrown.
        :return: string
        """
        countries = self.country_area.select_related('location').order_by('country_area_name')

        names = []
        for country in countries:
            name = country.country_area_name
            if name is None:
                continue
            iso_code = country.iso_alpha3_code

            name_and_code = ''.join([name, ' (', iso_code, ')'])
            if name_and_code not in names:
                names.append(name_and_code)

        return ', '.join(names)

    @property
    def region_names(self):
        """
        Returns a list of UNSD regions (names only) associated with a Heritage Site.
        Note that not all Heritage Sites are associated with a region. In such cases the
        Queryset will return as <QuerySet [None]> and the list will need to be checked for
        None or a TypeError (sequence item 0: expected str instance, NoneType found) runtime
        error will be thrown.
        :return: string
        """

        # Add code that uses self to retrieve a QuerySet composed of regions, then loops over it
        # building a list of region names, before returning a comma-delimited string of names.
        countries = self.country_area.select_related('location').order_by('location__region__region_name')

        regions = []
        for country in countries:
            region = country.location.region.region_name
            if region is None:
                continue

            if region not in regions:
                regions.append(region)

        return ', '.join(regions)

    @property
    def sub_region_names(self):
        """
        Returns a list of UNSD subregions (names only) associated with a Heritage Site.
        Note that not all Heritage Sites are associated with a subregion. In such cases the
        Queryset will return as <QuerySet [None]> and the list will need to be checked for
        None or a TypeError (sequence item 0: expected str instance, NoneType found) runtime
        error will be thrown.
        :return: string
        """

        # Add code that uses self to retrieve a QuerySet, then loops over it building a list of
        # sub region names, before returning a comma-delimited string of names using the string
        # join method.
        countries = self.country_area.select_related('location').order_by('location__sub_region__sub_region_name')

        sub_regions = []
        for country in countries:
            sub_region = country.location.sub_region.sub_region_name
            if sub_region is None:
                continue

            if sub_region not in sub_regions:
                sub_regions.append(sub_region)

        return ', '.join(sub_regions)


    @property
    def intermediate_region_names(self):
        """
        Returns a list of UNSD intermediate regions (names only) associated with a Heritage Site.
        Note that not all Heritage Sites are associated with an intermediate region. In such
        cases the Queryset will return as <QuerySet [None]> and the list will need to be
        checked for None or a TypeError (sequence item 0: expected str instance, NoneType found)
        runtime error will be thrown.
        :return: string
        """

        # Add code that uses self to retrieve a QuerySet, then loops over it building a list of
        # intermediate region names, before returning a comma-delimited string of names using the
        # string join method.

        countries = self.country_area.select_related('location').order_by('location__intermediate_region__intermediate_region_name')

        intermediate_regions = []
        for country in countries:
            try:
                intermediate_region = country.location.intermediate_region.intermediate_region_name
                if intermediate_region is None:
                    continue
            except:
                intermediate_region = ""

            if intermediate_region not in intermediate_regions:
                if intermediate_region != "":
                    intermediate_regions.append(intermediate_region)

        return ', '.join(intermediate_regions)


class HeritageSiteCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(unique=True, max_length=25)

    class Meta:
        managed = False
        db_table = 'heritage_site_category'
        ordering = ['category_name']
        verbose_name = 'UNESCO Heritage Site Category'
        verbose_name_plural = 'UNESCO Heritage Site Categories'

    def __str__(self):
        return self.category_name


class HeritageSiteJurisdiction(models.Model):
    heritage_site_jurisdiction_id = models.AutoField(primary_key=True)
    heritage_site = models.ForeignKey(HeritageSite, on_delete=models.CASCADE)
    country_area = models.ForeignKey(CountryArea, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'heritage_site_jurisdiction'
        ordering = ['heritage_site', 'country_area']
        verbose_name = 'UNESCO Heritage Site Jurisdiction'
        verbose_name_plural = 'UNESCO Heritage Site Jurisdictions'



class IntermediateRegion(models.Model):
    intermediate_region_id = models.AutoField(primary_key=True)
    intermediate_region_name = models.CharField(unique=True, max_length=100)
    sub_region = models.ForeignKey('SubRegion', on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'intermediate_region'
        ordering = ['intermediate_region_name']
        verbose_name = 'UNSD M49 Intermediate Region'
        verbose_name_plural = 'UNSD M49 Intermediate Regions'

    def __str__(self):
        return self.intermediate_region_name




class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(unique=True, max_length=100)
    planet = models.ForeignKey('Planet', on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'region'
        ordering = ['region_name']
        verbose_name = 'UNSD M49 Region'
        verbose_name_plural = 'UNSD M49 Regions'

    def __str__(self):
        return self.region_name



class SubRegion(models.Model):
    sub_region_id = models.AutoField(primary_key=True)
    sub_region_name = models.CharField(unique=True, max_length=100)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'sub_region'
        ordering = ['sub_region_name']
        verbose_name = 'UNSD M49 Subregion'
        verbose_name_plural = 'UNSD M49 Subregions'

    def __str__(self):
        return self.sub_region_name




class Planet(models.Model):
    """
    New model based on Mtg 5 refactoring of the database.
    """
    planet_id = models.AutoField(primary_key=True)
    planet_name = models.CharField(unique=True, max_length=10)
    unsd_name = models.CharField(unique=True, max_length=10)
    # define additional properties as needed    

    class Meta:
        managed = False   #<-- YOU MUST SET managed TO FALSE
        db_table = 'planet'
        ordering = ['planet_name']
        verbose_name = 'UMSD M49 Global'
        verbose_name_plural = 'UMSD M49 Globals'

    def __str__(self):
        return self.unsd_name #<-- MUST RETURN A STRING



class Location(models.Model):
    """
    New model based on Mtg 5 refactoring of the database.
    """
    location_id = models.AutoField(primary_key=True)
    planet = models.ForeignKey('Planet', on_delete=models.PROTECT)
    region = models.ForeignKey('Region', on_delete=models.PROTECT, blank=True, null=True)
    sub_region = models.ForeignKey('SubRegion', on_delete=models.PROTECT, blank=True, null=True)
    intermediate_region = models.ForeignKey('IntermediateRegion', on_delete=models.PROTECT, blank=True, null=True)
    # define additional properties as needed    

    class Meta:
        managed = False  # <-- YOU MUST SET managed TO FALSE
        db_table = 'location'
        ordering = ['planet', 'region', 'sub_region', 'intermediate_region']
        verbose_name = 'UMSD M49 Location Hierarchy'
        verbose_name_plural = 'UMSD M49 Location Hierarchies'

    def __str__(self):
        return '{} {} {} {}'.format(
            self.planet,
            self.region if self.region else '',
            self.sub_region if self.sub_region else '',
            self.intermediate_region if self.intermediate_region else '')





