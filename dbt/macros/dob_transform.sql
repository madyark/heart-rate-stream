-- Transforms date of birth values from YYYYMMDD in int format to YYYY-MM-DD in varchar

{% macro dob_transform(dob_column) %}
    to_date(cast({{ dob_column }} as varchar), 'YYYYMMDD') as {{ dob_column }}
{% endmacro %}
