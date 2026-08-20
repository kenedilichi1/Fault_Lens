import { create } from "zustand";

interface OrganizationUIState {
  isEditDialogOpen: boolean;
  isInviteDialogOpen: boolean;

  openEditDialog: () => void;
  closeEditDialog: () => void;

  openInviteDialog: () => void;
  closeInviteDialog: () => void;
}

export const useOrganizationUIStore =
  create<OrganizationUIState>((set) => ({
    isEditDialogOpen: false,
    isInviteDialogOpen: false,

    openEditDialog: () =>
      set({
        isEditDialogOpen: true,
      }),

    closeEditDialog: () =>
      set({
        isEditDialogOpen: false,
      }),

    openInviteDialog: () =>
      set({
        isInviteDialogOpen: true,
      }),

    closeInviteDialog: () =>
      set({
        isInviteDialogOpen: false,
      }),
  }));