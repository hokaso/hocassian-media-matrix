export default {
  /**
   * 功能描述：计算文本的长度
   * @param strKit
   * @returns {number}
   */
  getByteLen (strKit) {
    let len = 0
    if (typeof strKit === 'string' && strKit.constructor === String) {
      for (let i = 0; i < strKit.length; i++) {
        if (strKit[i].match(/[^x00-xff]/ig)) { // 全角
          len += 2
        } else {
          len += 1
        }
      }
    }
    return len
  }
}
