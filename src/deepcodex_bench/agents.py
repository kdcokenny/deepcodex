from __future__ import annotations

import logging
import shlex
from pathlib import Path
from typing import TYPE_CHECKING

from pier.agents.installed.codex import Codex
from pier.models.agent.network import NetworkAllowlist
from pier.models.task.config import MCPServerConfig

if TYPE_CHECKING:
    from pier.agents.base import AgentContext
    from pier.environments.base import BaseEnvironment


class LazyCodexStartWork(Codex):
    def __init__(
        self,
        logs_dir: Path,
        model_name: str | None = None,
        logger: logging.Logger | None = None,
        mcp_servers: list[MCPServerConfig] | None = None,
        skills_dir: str | None = None,
        prompt_template_path: Path | str | None = None,
        version: str | None = None,
        extra_env: dict[str, str] | None = None,
        command_model_name: str | None = None,
        config_toml: str | None = None,
        config_toml_file: str | None = None,
        reasoning_effort: str | None = None,
        reasoning_summary: str | None = None,
        lazycodex_package: str = "lazycodex-ai@latest",
        lazycodex_install_timeout_sec: int = 900,
    ) -> None:
        super().__init__(
            logs_dir=logs_dir,
            model_name=model_name,
            logger=logger,
            mcp_servers=mcp_servers,
            skills_dir=skills_dir,
            prompt_template_path=prompt_template_path,
            version=version,
            extra_env=extra_env,
            command_model_name=command_model_name,
            config_toml=config_toml,
            config_toml_file=config_toml_file,
            reasoning_effort=reasoning_effort,
            reasoning_summary=reasoning_summary,
        )
        self._lazycodex_package = lazycodex_package
        self._lazycodex_install_timeout_sec = lazycodex_install_timeout_sec

    def network_allowlist(self) -> NetworkAllowlist:
        allowlist = super().network_allowlist()
        return NetworkAllowlist(domains=sorted({*allowlist.domains, "registry.npmjs.org"}))

    async def run(
        self,
        instruction: str,
        environment: BaseEnvironment,
        context: AgentContext,
    ) -> None:
        original_exec_as_agent = self.exec_as_agent
        install_state = {"done": False}

        async def exec_as_agent_with_lazycodex(
            environment: BaseEnvironment,
            command: str,
            env: dict[str, str] | None = None,
            cwd: str | None = None,
            timeout_sec: int | None = None,
        ) -> object:
            result = await original_exec_as_agent(
                environment,
                command=command,
                env=env,
                cwd=cwd,
                timeout_sec=timeout_sec,
            )
            if not install_state["done"] and env and "CODEX_HOME" in env:
                install_state["done"] = True
                await original_exec_as_agent(
                    environment,
                    command=self._lazycodex_install_command(),
                    env=env,
                    cwd=cwd,
                    timeout_sec=self._lazycodex_install_timeout_sec,
                )
            return result

        self.exec_as_agent = exec_as_agent_with_lazycodex  # type: ignore[method-assign]
        try:
            await super().run(self._start_work_instruction(instruction), environment, context)
        finally:
            self.exec_as_agent = original_exec_as_agent  # type: ignore[method-assign]

    def _lazycodex_install_command(self) -> str:
        package = shlex.quote(self._lazycodex_package)
        return (
            "if [ -s ~/.nvm/nvm.sh ]; then . ~/.nvm/nvm.sh; fi\n"
            'export CODEX_HOME="${CODEX_HOME:?CODEX_HOME must be set}"\n'
            "if command -v bunx >/dev/null 2>&1; then\n"
            f"  bunx --yes {package} install --no-tui --codex-autonomous --skip-auth\n"
            "elif command -v npx >/dev/null 2>&1; then\n"
            f"  npx --yes {package} install --no-tui --codex-autonomous --skip-auth\n"
            "else\n"
            '  echo "Neither bunx nor npx is available for LazyCodex install" >&2\n'
            "  exit 127\n"
            "fi"
        )

    @staticmethod
    def _start_work_instruction(instruction: str) -> str:
        return f"$start-work\n\n{instruction}"
