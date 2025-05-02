import type { RouteLocationRaw } from "vue-router"

export type TileSliderData = {
  title: string
  subtitle?: string
  route?: RouteLocationRaw
  subtitleRoute?: RouteLocationRaw
}

export type TitleLevel = "h1" | "h2" | "h3" | "h4"

export type ItemSelect = {
  value: any
  title: string | number
}
