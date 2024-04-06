-- 
create stream hrdata (
    user_id int,
    heart_rate int,
    timestamp bigint,
    meta struct<
        activity_id int,
        location struct<
            latitude double,
            longitude double
        >
    >
) with (
    kafka_topic='hr-data-topic',
    value_format='json',
    timestamp='timestamp'
);