# dataemon

Simple daemon that runs [dbt](https://docs.getdbt.com/). The daemon reads a list of [DBT packages](https://docs.getdbt.com/docs/building-a-dbt-project/package-management) that you want to run from Postgres, and then executes these packages.

### Deployment

See [docker-compose.yml](./docker-compose.yml) for standard usage. All configuration is done through environment variables. Env var examples can be seen in [.env](./.env).

### Usage

Adding package for execution in daemon,

```
INSERT INTO $(POSTGRES_SCHEMA)._dataemon VALUES (
    NOW(), 'https://github.com/url/of/package.git', 'either-a-branch-or-commit'
)
```
