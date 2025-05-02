export type ContentPayload = {
  [key: string]: string
}

type Content = Record<string, ContentPayload>

export type TextLoaderPayload = {
  nl?: Content
  en?: Content
}

