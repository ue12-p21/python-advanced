# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
#     notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version,
#       -jupytext.text_representation.format_version, -language_info.version, -language_info.codemirror_mode.version,
#       -language_info.codemirror_mode, -language_info.file_extension, -language_info.mimetype,
#       -toc
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   language_info:
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#   nbhosting:
#     title: intro cours 8/9
#   rise:
#     autolaunch: true
#     slideNumber: c/t
#     start_slideshow_at: selected
#     theme: sky
#     transition: cube
#   version: '1.0'
# ---

# %% [markdown]
# # cours 8/9 : fonctions

# %% [markdown] tags=[]
# ## objectifs
#
# le programme pour aujourd'hui
#
# * étudier les objets de type fonction
#   * le passage de paramètre
#   * les fonctions comme citoyen de niveau 1

# %% [markdown]
# ## support PDF
#
# une [présentation de type slides au format pdf](media/les-fonctions.pdf)

# %% [markdown]
# ## vidéos
#
# 1. une vidéo sur le passage de paramètres
#
# <video width="800px" controls src="media/les-arguments-des-fonctions.mp4" type="video/mp4"></video>

# %% [markdown]
# 1. [Les arguments](https://youtu.be/8hLlyUbXZ3U)
# 1. [Les clôtures](https://youtu.be/msoWN4wSplM)
# 1. [La syntaxe lambda](https://youtu.be/Rsu9O1soTsA)
# 1. [Les générateurs](https://youtu.be/DqYM_XMVtKw)
#
# <!-- bien sûr ça marche pas car la page est une vraie page web
#      mais même avec /embed ajouté non plus
#      on dirait bien que YT fait tout pour qu'on ne puisse pas faire comme ça
#
# <video width="800px" controls src="https://youtu.be/8hLlyUbXZ3U" type="video/mp4"></video>
#
# <video width="800px" controls src="https://youtu.be/msoWN4wSplM" type="video/mp4"></video>
#
# <video width="800px" controls src="https://youtu.be/Rsu9O1soTsA" type="video/mp4"></video>
#
# <video width="800px" controls src="https://youtu.be/DqYM_XMVtKw" type="video/mp4"></video>
# -->

# %% [markdown]
# ## les solutions
#
# comme toujours dans
#
# https://github.com/ue12-p21/python-advanced-solutions
