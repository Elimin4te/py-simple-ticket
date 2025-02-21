from dataclasses import dataclass, field
from typing_extensions import Self

@dataclass
class MenuChild:

    title: str
    """Child menu entry."""
    href: str
    """Target link where this child points to."""


@dataclass
class MenuEntry:

    tag: str
    """Internal tag of this entry."""
    title: str
    """Navigation entry title."""
    icon: str
    """FontAwesome icon."""
    href: str = None
    """Target link where this entry points to (invalid if this item has childs)."""
    breadcrumbs: str = None
    """point (.) separated breadcrumb definition for this entry."""
    position: int = 10
    """Entry position in the menu."""
    is_active: bool = False
    """Set's the entry as active in the frontend."""
    childs: list[MenuChild] = field(default_factory=list)
    """Children entries of this list."""

    @property
    def has_childs(self):
        return len(self.childs) > 0

    def add_child(self, child: MenuChild):
        self.childs.append(child)

    def __post_init__(self):
        if self.breadcrumbs:
            self.breadcrumbs = [bc.capitalize() for bc in self.breadcrumbs.split('.')]

    def __eq__(self, other: Self) -> bool:
        return self.tag == other.tag


class Menu:
    """ Represents the app menu, the entries in this class will be used to build the frontend. """

    __instance__ = None

    def __init__(self) -> None:
        self.entries: list[MenuEntry] = []
        self.active_entry: MenuEntry = None
        self.__instance__ = self

    def add_entry(self, entry: MenuEntry):
        self.entries.append(entry)
        self.sort_entries()

    def set_entry_active(self, entry_tag: str):
        """Deactivates all entries and set the specified one as the only active one."""

        for entry in self.entries:
            entry.is_active = False

        entry = tuple(filter(lambda e: e.tag == entry_tag, self.entries))
        assert len(entry), f"An entry with the {entry_tag} tag doesn't exists."
        entry_index = self.entries.index(entry[0])

        self.entries[entry_index].is_active = True
        self.active_entry = entry[0]

    def sort_entries(self):
        self.entries = list(sorted(self.entries, key=lambda e: e.position))

    def __new__(cls: type[Self], *args, **kwargs) -> Self:

        if cls.__instance__:
            return cls.__instance__

        return super().__new__(cls, *args, **kwargs)
        
app_menu = Menu()