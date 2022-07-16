from typing import Final
from pyteal import *
from beaker.application import Application
from beaker.application_schema import DynamicApplicationStateValue
from beaker.decorators import handler


class ARC21(Application):
    """Interface for a round based datafeed oracle"""

    @Subroutine(TealType.bytes)
    def round_key(round):
        return Concat(Bytes("data:"), Itob(round))

    data_for_round: Final[DynamicApplicationStateValue] = DynamicApplicationStateValue(
        stack_type=TealType.bytes, max_keys=64, key_gen=round_key
    )

    @handler
    def get(
        self,
        round: abi.Uint64,
        user_data: abi.DynamicArray[abi.Byte],
        *,
        output: abi.DynamicArray[abi.Byte]
    ):
        return output.decode(self.data_for_round(round.get()))

    @handler
    def mustGet(
        self,
        round: abi.Uint64,
        user_data: abi.DynamicArray[abi.Byte],
        *,
        output: abi.DynamicArray[abi.Byte]
    ):
        return output.decode(self.data_for_round(round.get()).get_must())
