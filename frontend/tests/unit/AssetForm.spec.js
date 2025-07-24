import { mount } from '@vue/test-utils'
import AssetForm from '@/components/forms/AssetForm.vue'

describe('AssetForm', () => {
  it('rende il form asset', () => {
    const wrapper = mount(AssetForm, {
      props: { sites: [], assetTypes: [], allLocations: [], manufacturers: [], assetStatusOptions: [] }
    })
    expect(wrapper.text()).toContain('Caricamento dati...')
  })
}) 