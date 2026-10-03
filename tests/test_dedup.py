from sentiment_drift.ingestion.dedup import deduplicate_records


def test_deduplicate_records_filters_existing_and_in_batch_duplicates():
    records = [{"id": "a"}, {"id": "b"}, {"id": "b"}, {"id": "c"}]
    new_records, skipped = deduplicate_records(records, existing_ids={"a"})

    assert [r["id"] for r in new_records] == ["b", "c"]
    assert skipped == 2
