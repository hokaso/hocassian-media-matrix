const getters = {
  device: state => state.app.device,
  permission_routes: state => state.permission.routes,
  isMobile: state => state.app.isMobile,
  about: state => state.about.info,
}
export default getters
