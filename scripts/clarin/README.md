util-scripts
===========

This directory contains some utility scripts.

## findMapping.sh

CLARIN's [CMD Infrastructure](http://www.clarin.eu/cmdi/) allows very heterogenously structured metadata records. The structures are govermed by metadata profiles, which are annotated by ConceptLinks. The [Virtual Language Observatory](http://www.clarin.eu/vlo/) (VLO) facetted browser has a [mapping file](https://lux17.mpi.nl/isocat/clarin/vlo/mapping/facetConcepts.xml) to map concepts or XPaths to its facets. The findMappings.sh utility can use this CLARIN mapping file to generate a DASISH map file.

As input it needs

* a directory containing the CMD records to analyze which metadata profiles are used
* a template map file
* a directory to temporarily store the metadata profiles

A list of all parameters and their defaults can be obtained by running:

```sh
./findMapping.sh -h
```
	
### Template map file

In the template map file a facet can

1. refer to one or more VLO facets to indicate that its CLARIN mapping should be used
2. refer to concepts to indicate that a DASISH specific mapping should be generated

#### Refer to one or more VLO facets

```xml
<mapping-table xmlns:cmd="http://www.clarin.eu/cmd/">
  ...
  <field name="Language" cmd:facetConcepts="language languageCode languages">
    <cmd:facet>language</cmd:facet>
    <cmd:facet>languageCode</cmd:facet>
    <cmd:facet>languages</cmd:facet>
  </field>
  ...
</mapping-table>
```

#### Refer to a concept

```xml
<mapping-table xmlns:cmd="http://www.clarin.eu/cmd/">
  ...
  <field name="url">
    ...
    <cmd:concept>http://www.isocat.org/datcat/DC-2546</cmd:concept>
    ...
  </field>
  ...
</mapping-table>
```
    
#### Allow multiple values

When multiple values are allowed findMapping.sh will generate one XPath per metadata profile which combines possible XPaths by a `string-join(distinct-values(...),';')`.

When refering to a concept allow multiple values can be switched off (on is the default) by adding `@cmd:allowedMultipleValues="false"` to the field element.

#### Order of XPaths

The XPaths found by the facet/concept mapping get inserted into the place where the corresponding element is found. This makes it possible to insert default DASISH mappings that will overrule the CLARIN mappings.


### Notes

This tools mimics the VLO mapping from concepts to facets, but its not completely inline. The VLO also supports blacklist patters, which this tool doesn't support yet.

## xsl2

Shell wrapper around the Saxon Java libraries. See the [Saxon documentation](http://saxonica.com/documentation/html/using-xsl/commandline.html) for a description of the commandline.