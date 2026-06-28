/**
 * LocalStorage 历史记录
 */
const KEY = 'qr-history'
const MAX = 10

export function loadHistory() {
  try {
    const raw = localStorage.getItem(KEY)
    return raw ? JSON.parse(raw) : []
  } catch (e) {
    return []
  }
}

export function saveHistoryItem(item) {
  const list = loadHistory()
  list.unshift({ ...item, at: Date.now() })
  const trimmed = list.slice(0, MAX)
  try { localStorage.setItem(KEY, JSON.stringify(trimmed)) } catch (e) {}
  return trimmed
}

export function clearHistory() {
  try { localStorage.removeItem(KEY) } catch (e) {}
}

export function removeHistoryItem(id) {
  const list = loadHistory().filter(it => it.id !== id)
  try { localStorage.setItem(KEY, JSON.stringify(list)) } catch (e) {}
  return list
}
