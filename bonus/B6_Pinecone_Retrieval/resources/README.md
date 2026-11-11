# B6 resources

`labB6_managed_store.mmd` is the source of the diagram shown in the notebook; `labB6_managed_store.png` is its exported image. Ink marks the embedding model, lime marks our code, and white marks data or a database service.

The notebook reads the 36 supplied teaching fixtures from `../../../data/corpus/` in place. It bundles no duplicate corpus, embeddings or credentials. File IDs and `kind` metadata match Lab 12. See the repository's [data note](../../../data/README.md) for their provenance. The policies and tickets are supplied teaching material under this repository's terms; no separate dataset licence is asserted here.

The ten question labels are included directly in both notebooks. They name the file that answers each question; two questions have no answer. The same returned embedding arrays are used for Pinecone and Chroma within a run.

The relevant APIs were checked against the official Pinecone Python SDK documentation: [schema and upsert](https://sdk.pinecone.io/python/how-to/documents/schema-and-upsert.html), [search](https://sdk.pinecone.io/python/how-to/documents/search.html), and [v10 migration](https://sdk.pinecone.io/python/migration/v10-migration.html). The notebook uses the schema/documents API, rather than the older dimension/spec compatibility calls. Account availability and charges are governed by the live [pricing page](https://www.pinecone.io/pricing/) and the learner's account.
