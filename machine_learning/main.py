def main():
    wrapper = MatchingEngineWrapper(
        project="my-gcp-project",
        location="us-central1",
        key_path="path/to/service-account.json",
    )

    # 1) List esistenti
    existing = wrapper.list_indexes(filter='display_name="my_streaming_index"')
    idx = existing[0] if existing else None

    # 2) Crea se non esiste
    if not idx:
        idx = wrapper.create_index(
            display_name="my_streaming_index",
            contents_delta_uri="gs://my_bucket/initial_embeddings/",
            dimensions=768,
            labels={"env": "dev"}
        )

    # 3) Upsert di nuovi datapoint
    wrapper.upsert_datapoints(idx, [
        {"id": "dp1", "embedding": [0.1, 0.2, 0.3]},
        {"id": "dp2", "embedding": [0.4, 0.5, 0.6], "restricts": [{"namespace": "tag", "allow": ["blue"]}]}
    ])

    # 4) Remove di un datapoint
    wrapper.remove_datapoints(idx, ["dp1"])

    # 5) Aggiorna metadata dell'indice
    wrapper.update_metadata(idx, display_name="my_updated_index", labels={"env": "prod"})

    # 6) Aggiorna embeddings in bulk (delta)
    wrapper.update_embeddings(idx, contents_delta_uri="gs://my_bucket/delta_embeddings/", is_complete_overwrite=False)

    # 7) Update embeddings con overwrite completo
    wrapper.update_embeddings(idx, contents_delta_uri="gs://my_bucket/full_embeddings/", is_complete_overwrite=True)

if __name__ == "__main__":
    main()
