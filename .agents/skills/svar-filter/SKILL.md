---
name: svar-filter
# prettier-ignore
description: SVAR Svelte Filter for complex table filtering with visual query builder and nested logic.
---

# SVAR Svelte Filter

## Quick Start

**Installation:**
```bash
bun add @svar/filter
```

**Components:**
- `FilterBuilder` - Visual query builder with nested AND/OR logic
- `FilterEditor` - Single-field filter editor
- `FilterBar` - Lightweight quick filter toolbar

## When to Use

**Use SVAR Filter for:**
- ✅ Multi-field filtering with complex logic (AND/OR groups)
- ✅ Date range filtering
- ✅ Dynamic filter UI (users build their own queries)
- ✅ Advanced search with nested conditions

**Use simple input filters for:**
- ❌ Single field search
- ❌ Basic dropdown filters
- ❌ Static filter options

## Basic Usage with Grid

```typescript
<script lang="ts">
  import { Grid } from '@svar/grid'
  import { FilterBuilder } from '@svar/filter'

  let data = $state([...])
  let filterValue = $state(null)

  // Reactive filtered data
  const filteredData = $derived(
    filterValue ? applyFilter(data, filterValue) : data
  )

  const columns = [
    { id: 'name', header: 'Name' },
    { id: 'email', header: 'Email' },
    { id: 'status', header: 'Status' },
  ]

  const filterConfig = {
    fields: [
      { name: 'name', label: 'Partner Name', type: 'text' },
      { name: 'email', label: 'Email', type: 'text' },
      { name: 'status', label: 'Status', type: 'select', options: ['active', 'inactive'] },
      { name: 'created_at', label: 'Created Date', type: 'date' },
    ]
  }
</script>

<FilterBuilder
  config={filterConfig}
  bind:value={filterValue}
/>

<Grid data={filteredData} {columns} />
```

## Filter Components

### FilterBuilder
Visual query builder for complex logic:
- Nested filter groups
- AND/OR logic between groups
- Multiple conditions per field
- Add/remove rules dynamically

### FilterBar
Compact toolbar for quick filtering:
- Horizontal or vertical layout
- Compact mode
- Pre-defined filter sets

### FilterEditor
Single-field filter:
- Text matching (contains, begins with, equals)
- Number comparison (>, <, =, between)
- Date ranges

## Filter Types

**Supported data types:**
- Text (contains, begins with, equals, not equals)
- Number (>, <, =, ≠, between)
- Date (before, after, between, equals)
- Select (equals, not equals, in list)

## Advanced: Backend Integration

Transform filter to SQL for backend filtering:

```typescript
// Server-side (Remote Function)
import { filterToSQL } from '@svar/filter'

export const getFilteredPartners = async (filter: FilterValue) => {
  const sqlWhere = filterToSQL(filter)
  // Use with Drizzle query builder
  return db.select().from(partners).where(sql`${sqlWhere}`)
}
```

## BUIS Integration Pattern

```typescript
// lib/components/partners/PartnerListWithFilter.svelte
<script lang="ts">
  import { Grid } from '@svar/grid'
  import { FilterBuilder } from '@svar/filter'
  import { getFilteredPartners } from '$lib/server/partners/functions'
  import { createQuery } from '$lib/components/shared/createQuery.svelte.ts'

  let filterValue = $state(null)

  // Auto-refetch when filter changes
  const partners = createQuery(() => getFilteredPartners(filterValue))
</script>

<div class="space-y-4">
  <FilterBuilder config={filterConfig} bind:value={filterValue} />

  {#if partners.loading}
    <Skeleton />
  {:else if partners.data}
    <Grid data={partners.data} {columns} />
  {/if}
</div>
```

## Customization

**Themes:**
- Light and dark mode support
- CSS variables for styling
- Tailwind integration

**Localization:**
- Configurable labels
- Multi-language support

## Resources

- Official Docs: https://docs.svar.dev/svelte/filter/filter-main-overview/
- Grid Integration: See `svar-grid` skill
- TypeScript support: Built-in types
- License: MIT

**Last verified:** 2025-12-30
