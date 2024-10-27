from datasources import isearchd_provider
from presentation import cli_executor_impl
from domain.executor import CLIExecutor


def Init() -> CLIExecutor:
    provider = isearchd_provider.SearchProviderImpl()
    executor = cli_executor_impl.CLIExecutorImpl(provider)
    return executor
