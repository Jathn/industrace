# CriticalityBadge Component

Il componente `CriticalityBadge` è utilizzato per visualizzare la criticità aziendale degli asset con badge colorati, simile al design del badge dello stato degli asset. Include icone e testo con sfondo colorato per massima visibilità.

## Utilizzo

```vue
<template>
  <!-- Versione completa con icona e testo -->
  <CriticalityBadge :value="asset.business_criticality" />
  
  <!-- Solo icona -->
  <CriticalityBadge :value="asset.business_criticality" :iconOnly="true" />
  
  <!-- Solo testo (senza icona) -->
  <CriticalityBadge :value="asset.business_criticality" :showIcon="false" />
</template>
```

## Props

| Prop | Tipo | Default | Descrizione |
|------|------|---------|-------------|
| `value` | String | required | Il valore della criticità ('low', 'medium', 'high', 'critical') |
| `showIcon` | Boolean | true | Mostra l'icona |
| `showText` | Boolean | true | Mostra il testo |
| `iconOnly` | Boolean | false | Mostra solo l'icona (ignora showText) |

## Valori Supportati

| Valore | Icona | Colore | Descrizione |
|--------|-------|--------|-------------|
| `low` | `pi pi-circle-fill` | Verde (#28a745) | Criticità bassa |
| `medium` | `pi pi-exclamation-circle` | Giallo (#ffc107) | Criticità media |
| `high` | `pi pi-exclamation-triangle` | Arancione (#fd7e14) | Criticità alta |
| `critical` | `pi pi-times-circle` | Rosso (#dc3545) | Criticità critica |
| Altri | `pi pi-question-circle` | Grigio (#6c757d) | Valore non riconosciuto |

## Esempi di Utilizzo

### Tabella Assets
```vue
<template #body-business_criticality="{ data }">
  <CriticalityBadge :value="data.business_criticality" />
</template>
```

### Dashboard (versione compatta)
```vue
<template #body="{ data }">
  <CriticalityBadge :value="data.business_criticality" :iconOnly="true" />
</template>
```

### Dettaglio Asset
```vue
<div class="asset-info">
  <span class="label">Criticità:</span>
  <CriticalityBadge :value="asset.business_criticality" />
</div>
```

## Stili CSS

Il componente include i seguenti stili:

```css
.criticality-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #fff;
  background: v-bind(criticalityColor);
}

.criticality-badge i {
  font-size: 0.875rem;
}

.criticality-text {
  font-weight: 500;
}

.criticality-badge.icon-only {
  gap: 0;
  padding: 0.2rem;
}

.criticality-badge.icon-only i {
  font-size: 1rem;
}
```

Il design è simile al badge dello stato degli asset, con sfondo colorato e testo bianco per massima visibilità.

## Localizzazione

Il componente utilizza le seguenti chiavi di traduzione:

- `assets.businessCriticalityLow` → "Bassa"
- `assets.businessCriticalityMedium` → "Media" 
- `assets.businessCriticalityHigh` → "Alta"
- `assets.businessCriticalityCritical` → "Critica"
- `common.na` → "N/A"

## Note

- Il componente gestisce automaticamente i valori null/undefined mostrando "-"
- I valori sono case-insensitive (es. "HIGH" = "high")
- Le icone utilizzano PrimeVue Icons
- I colori seguono la palette Bootstrap per consistenza 