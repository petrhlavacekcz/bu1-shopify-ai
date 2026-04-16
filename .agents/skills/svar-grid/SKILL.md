---
name: svar-grid
# prettier-ignore
description: SVAR Svelte DataGrid for complex data tables with virtual scrolling, filtering, sorting, and editing.
---

# SVAR Svelte DataGrid

## Quick Start

**Installation:**
```bash
bun add @svar/grid
```

**When to use SVAR Grid instead of shadcn Table:**
- ✅ Complex tables with 100+ rows (virtual scrolling)
- ✅ Advanced filtering and multi-column sorting
- ✅ In-cell editing with validation
- ✅ Column resizing, hiding, pinning
- ✅ Tree data or hierarchical structures
- ✅ Pagination with large datasets

**Use shadcn Table for:**
- ❌ Simple displays (< 50 rows, no editing)
- ❌ Static data presentations
- ❌ Basic sorting only

## Basic Usage

```typescript
<script lang="ts">
  import { Grid } from '@svar/grid'

  // Data binding with Svelte 5 Runes
  let data = $state([
    { id: 1, name: 'Partner A', email: 'a@example.com', status: 'active' },
    { id: 2, name: 'Partner B', email: 'b@example.com', status: 'inactive' },
  ])

  const columns = [
    { id: 'name', header: 'Name', width: 200 },
    { id: 'email', header: 'Email', width: 250 },
    { id: 'status', header: 'Status', width: 120 },
  ]
</script>

<Grid {data} {columns} />
```

## Key Features

**Data Operations:**
- In-cell editing with built-in editors
- Column header filtering
- Single and multi-column sorting
- Row selection (single/multiple)
- Row reordering (drag & drop)
- Context menus
- Undo/redo functionality

**Performance:**
- Virtual scrolling (rows and columns)
- Dynamic data loading
- Handles 10,000+ rows smoothly

**Configuration:**
- Colspan and rowspan support
- Collapsible column groups
- Pinned columns (freeze)
- Drag-and-drop column resizing
- Auto-sizing columns
- Responsive mode
- Localization support
- Theme support (CSS variables)

## Integration with BUIS

**Domain Components Pattern:**
```typescript
// lib/components/partners/PartnerGrid.svelte
<script lang="ts">
  import { Grid } from '@svar/grid'
  import type { Partner } from '$lib/server/partners/schema'

  interface Props {
    partners: Partner[]
    onEdit?: (partner: Partner) => void
    onDelete?: (id: string) => void
  }

  let { partners, onEdit, onDelete }: Props = $props()

  const columns = [
    { id: 'name', header: 'Partner Name', width: 250, editable: true },
    { id: 'email', header: 'Email', width: 300 },
    { id: 'created_at', header: 'Created', width: 150, type: 'date' },
  ]
</script>

<Grid
  data={partners}
  {columns}
  on:change={handleEdit}
  on:rowClick={handleRowClick}
/>
```

## With SVAR Filter

See `svar-filter` skill for integration with FilterBuilder and FilterBar.

## Resources

- Official Docs: https://docs.svar.dev/svelte/grid/overview
- TypeScript support: Built-in type definitions
- License: MIT

**Last verified:** 2025-12-30
