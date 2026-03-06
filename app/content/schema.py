from pydantic import AliasGenerator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel, to_snake


class MsczContentCreate(BaseModel):
    c_mscz_file_id: int
    c_svg_file_id: int
    pdf_file_id: int
    mp3_file_id: int | None = None

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )


class MsczContentRead(BaseModel):
    id: int
    c_mscz_file_id: int
    c_svg_file_id: int
    pdf_file_id: int
    mp3_file_id: int | None = None
    svg_url: str | None = None
    pdf_url: str | None = None
    mscz_url: str | None = None
    mp3_url: str | None = None
    added_at: str | None = None

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
    )
