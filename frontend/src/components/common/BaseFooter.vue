<template>
  <footer class="footer">
    <span class="footer-content">
      <img src="@/assets/logo_besafe.png" alt="BeSafe logo" class="besafe-logo" />
      <span>{{ $t('common.footer.powered_by') }}</span>
      <a :href="'https://www.besafe.it'" target="_blank" rel="noopener" class="besafe-link">
        {{ $t('common.footer.visit_besafe') }}
      </a>
    </span>
  </footer>
</template>

<script>
export default {
  name: "BaseFooter"
};
</script>

<style scoped>
.footer {
  width: 100%;
  text-align: center;
  padding: 1rem 0;
  color: #888;
  font-size: 0.95rem;
  background: #f8f8f8;
  border-top: 1px solid #eee;
}
.footer-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}
.besafe-logo {
  height: 28px;
  margin-right: 0.5rem;
  vertical-align: middle;
}
.besafe-link {
  margin-left: 0.5rem;
  color: #1976d2;
  text-decoration: underline;
  font-weight: 500;
}
.besafe-link:hover {
  color: #0d47a1;
}
</style> 