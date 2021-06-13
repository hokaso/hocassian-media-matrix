import { showRouteList } from '@/router'

/**
 * Use meta.role to determine if the current user has permission
 * @param roles
 * @param route
 */

const state = {
  routes: showRouteList,
}

export default {
  namespaced: true,
  state,
}
