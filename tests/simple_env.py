# Copyright 2022-2023 OmniSafe Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Simplest environment for testing."""

from __future__ import annotations

import random
from typing import Any

import torch
from gymnasium import spaces

from omnisafe.envs.core import CMDP, env_register


@env_register
class SimpleEnv(CMDP):
    """Simplest environment for testing."""

    _support_envs = ['Simple-v0']
    need_auto_reset_wrapper = True
    need_time_limit_wrapper = True
    _num_envs = 1

    def __init__(self, env_id: str, **kwargs) -> None:
        self._observation_space = spaces.Box(low=-1.0, high=1.0, shape=(3,))
        self._action_space = spaces.Box(low=-1.0, high=1.0, shape=(2,))

    def step(
        self,
        action: torch.Tensor,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, dict]:
        obs = torch.as_tensor(self._observation_space.sample())
        reward = torch.as_tensor(random.random())
        cost = torch.as_tensor(random.random())
        termiated = torch.as_tensor(random.random() > 0.5)
        truncated = torch.as_tensor(random.random() > 0.5)
        return obs, reward, cost, termiated, truncated, {}

    def reset(self, seed: int | None = None) -> tuple[torch.Tensor, dict]:
        if seed is not None:
            self.set_seed(seed)
        obs = torch.as_tensor(self._observation_space.sample())
        return obs, {}

    def set_seed(self, seed: int) -> None:
        random.seed(seed)

    def sample_action(self) -> torch.Tensor:
        return torch.as_tensor(self._action_space.sample())

    def render(self) -> Any:
        raise NotImplementedError

    def close(self) -> None:
        pass
