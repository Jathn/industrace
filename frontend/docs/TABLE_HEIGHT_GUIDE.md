# Guida all'Altezza delle Tabelle

## Panoramica

Le tabelle in Industrace ora supportano un'altezza dinamica che si adatta automaticamente allo spazio disponibile, ottimizzando l'uso dello schermo con il menu laterale.

## Funzionalità Disponibili

### 1. Altezza Fissa (Default)
```vue
<BaseDataTable
  :data="data"
  :columns="columns"
  :scrollHeight="'80vh'"
/>
```

### 2. Altezza Automatica (Raccomandata)
```vue
<BaseDataTable
  :data="data"
  :columns="columns"
  :autoHeight="true"
  :heightOffsetTop="200"
  :heightOffsetBottom="120"
/>
```

## Parametri di Configurazione

### `autoHeight` (Boolean)
- **Default**: `false`
- **Descrizione**: Abilita il calcolo automatico dell'altezza

### `heightOffsetTop` (Number)
- **Default**: `200`
- **Descrizione**: Spazio da riservare sopra la tabella (header, filtri, etc.)
- **Unità**: Pixel

### `heightOffsetBottom` (Number)
- **Default**: `100`
- **Descrizione**: Spazio da riservare sotto la tabella (footer, paginazione, etc.)
- **Unità**: Pixel

### `scrollHeight` (String)
- **Default**: `'80vh'`
- **Descrizione**: Altezza fissa quando `autoHeight` è `false`
- **Formati**: `'80vh'`, `'600px'`, `'100%'`

### `forceScroll` (Boolean)
- **Default**: `false`
- **Descrizione**: Forza l'abilitazione dello scroll indipendentemente dal calcolo automatico

## Esempi di Utilizzo

### Pagina Semplice (Header + Tabella)
```vue
<BaseDataTable
  :autoHeight="true"
  :heightOffsetTop="150"
  :heightOffsetBottom="100"
/>
```

### Pagina Complessa (Header + Filtri + Tabella + Azioni)
```vue
<BaseDataTable
  :autoHeight="true"
  :heightOffsetTop="300"
  :heightOffsetBottom="120"
/>
```

### Pagina con Tree View (Sites)
```vue
<BaseDataTable
  :autoHeight="true"
  :heightOffsetTop="300"
  :heightOffsetBottom="120"
/>
```

## Miglioramenti Implementati

### 1. Altezza di Default Aumentata
- **Prima**: `60vh`
- **Dopo**: `80vh`

### 2. Paginazione Ottimizzata
- **Righe di default**: 15 (bilanciato per schermi normali)
- **Opzioni**: [10, 15, 25, 50] (più realistiche)
- **Calcolo intelligente**: Considera le righe visibili vs righe richieste
- **Standardizzazione**: Tutte le pagine usano i default globali

### 3. Calcolo Dinamico
- Si adatta automaticamente alle dimensioni dello schermo
- Rispetta i limiti minimi e massimi
- Si aggiorna al resize della finestra
- **Scroll intelligente**: Abilita lo scroll solo quando necessario

## Best Practices

### 1. Utilizzare `autoHeight` per le pagine principali
```vue
<!-- ✅ Raccomandato -->
<BaseDataTable :autoHeight="true" />

<!-- ❌ Non ottimale -->
<BaseDataTable :scrollHeight="'60vh'" />
```

### 2. Calcolare gli offset in base al contenuto
- **Header semplice**: 150-200px
- **Header + filtri**: 200-250px
- **Header + filtri + tree**: 250-300px

### 3. Considerare il footer
- **Footer discreto**: 100-120px
- **Footer con azioni**: 120-150px

## Compatibilità

- ✅ **Desktop**: Ottimizzato per schermi grandi
- ✅ **Tablet**: Si adatta automaticamente
- ✅ **Mobile**: Mantiene usabilità su schermi piccoli

## Troubleshooting

### Tabella troppo alta
```vue
<BaseDataTable
  :autoHeight="true"
  :heightOffsetTop="300"  <!-- Aumentare -->
  :heightOffsetBottom="150"  <!-- Aumentare -->
/>
```

### Tabella troppo bassa
```vue
<BaseDataTable
  :autoHeight="true"
  :heightOffsetTop="100"  <!-- Diminuire -->
  :heightOffsetBottom="80"  <!-- Diminuire -->
/>
```

### Disabilitare completamente
```vue
<BaseDataTable
  :autoHeight="false"
  :scrollHeight="'600px'"
/>
```

### Forzare lo scroll
```vue
<BaseDataTable
  :autoHeight="true"
  :forceScroll="true"
/>
``` 