from typing import Optional, Tuple, Dict, Union, List, Set

from pydantic import BaseModel, HttpUrl


class Menu(BaseModel):
    name: str
    # whether is it a title or a model resource.
    title: Optional[bool]
    # must be format with /rest/<Model> if it's a model resource.
    url: Optional[str]
    icon: Optional[str]
    # children menu
    children: Optional[List['Menu']] = []
    # include fields
    include: Optional[Tuple[str]]
    # exclude fields
    exclude: Optional[Tuple[str]]
    # external link
    external: Optional[bool] = False
    # raw id fields
    raw_id_fields: Optional[Tuple[str]] = set()
    # searchable fields
    search_fields: Optional[Tuple[str]] = set()
    # sortable fields
    sort_fields: Optional[Set[str]] = set()
    # define field type,like select,radiolist,text,date
    fields_type: Dict = {}
    # define field attr,like cols which in bootstrap table
    attrs: Dict[str, Dict] = {}
    # active table export
    export: bool = True
    actions: Optional[Dict]
    bulk_actions: List[Dict] = [{
        'value': 'delete',
        'text': 'delete_all',
    }]


Menu.update_forward_refs()


class Site(BaseModel):
    name: str
    logo: HttpUrl
    login_logo: Optional[HttpUrl]
    login_footer: Optional[str]
    login_description: Optional[str]
    footer: Optional[str]
    locale: str
    locale_switcher: bool = False
    theme_switcher: bool = False
    theme: Optional[str]
    url: Optional[HttpUrl]
    grid_style: int = 1
    # custom css
    css: Optional[List[HttpUrl]]
    # menu define
    menus: Optional[List[Menu]]
    # custom footer with html
    footer: Optional[str]


class Field(BaseModel):
    label: str
    cols: Optional[int]
    input_cols: Optional[int]
    group: Optional[str]
    type: str
    required: bool = True
    options: Optional[List[Dict]]
    sortable: Optional[bool]
    multiple: bool = False
    ref: Optional[str]
    description: Optional[str]
    disabled: Optional[bool] = False


class Resource(BaseModel):
    title: str
    pk: str
    resource_fields: Dict[str, Union[Field, Dict]]
    searchFields: Optional[Dict[str, Field]]
    bulk_actions: Optional[List[Dict]]
    export: bool

    class Config:
        fields = {
            'resource_fields': 'fields',
        }
