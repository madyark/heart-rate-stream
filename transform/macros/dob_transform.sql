-- Transforms date of birth values from YYYYMMDD in int format to YYYY-MM-DD in varchar

{% macro dob_transform(dob_column) %}
    TO_DATE(CAST({{ dob_column }} AS VARCHAR), 'YYYYMMDD') AS {{ dob_column }}
{% endmacro %}
