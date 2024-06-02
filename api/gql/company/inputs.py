from typing import Annotated

import strawberry


@strawberry.input
class CreateCompanyInput:
    name: Annotated[
        str, strawberry.argument(description="The company's new name")]
