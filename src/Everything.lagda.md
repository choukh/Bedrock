# Bedrock

<!--en-->
*Laying the groundwork for the metaphysics of V.*

A machine-checked development, in Cubical Agda, of the set theory underlying contemporary
questions about the universe of sets: forcing, inner models, and the structure of V. The
immediate target is a full mechanization of `L` ⊨ GCH, with the cumulative hierarchy `V`
realised as a higher inductive type. The full treatment is in the
[Charter](https://github.com/choukh/Bedrock/blob/main/docs/en/CHARTER.md).

This site is generated from literate Agda. The development has no substantial content yet;
the modules below are examples that exercise the rendering framework. Browse them from the
sidebar, or in the import list below.
<!--zh-->
*为 V 的形而上学奠基。*

一项在 Cubical Agda 中的机器验证工作，针对当代集合宇宙问题背后的那部分集合论：力迫、内模型，以及 V 的结构。当前目标是完整机械化 `L` ⊨ GCH，其中累积层级 `V` 以高阶归纳类型实现。完整论述见 [纲领](https://github.com/choukh/Bedrock/blob/main/docs/zh/CHARTER.md)。

本站点由文学化 Agda 生成。开发尚无实质内容，下列模块是演示渲染框架的示例。可从侧边栏或下方的导入列表中浏览它们。
<!--/-->

```agda
{-# OPTIONS --cubical --safe --guardedness #-}
module Everything where

import HelloWorld
import Example.Naturals
import Example.Doubling
```
