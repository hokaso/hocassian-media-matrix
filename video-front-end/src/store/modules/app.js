const state = {
  device: "desktop",
  isMobile: document.body.clientWidth <= 768 ? true : false
};

const mutations = {
  TOGGLE_DEVICE: (state, device) => {
    state.device = device;
  }
};

const actions = {
  toggleDevice({ commit }, device) {
    commit("TOGGLE_DEVICE", device);
  }
};

export default {
  namespaced: true,
  state,
  mutations,
  actions
};
