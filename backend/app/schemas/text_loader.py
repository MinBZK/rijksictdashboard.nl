from pydantic import BaseModel, RootModel


class ContentPayload(BaseModel):
    content: str


Content = RootModel[dict[str, ContentPayload]]
Payload = RootModel[dict[str, Content]]
# class Content(BaseModel):
#     __root__: dict[str, ContentPayload]


# class Payload(BaseModel):
#     __root__: dict[str, Content]
