import {
  LAB_DB_NAME,
  LAB_SCHEMA_VERSION,
  LAB_STORE_NAME,
  importScenario,
  type TerritorialScenario,
} from './scenario-v2';

export class ScenarioStore {
  private open() {
    return new Promise<IDBDatabase>((resolve, reject) => {
      const request = indexedDB.open(LAB_DB_NAME, LAB_SCHEMA_VERSION);
      request.onupgradeneeded = () => {
        const db = request.result;
        if (!db.objectStoreNames.contains(LAB_STORE_NAME)) db.createObjectStore(LAB_STORE_NAME, { keyPath: 'id' });
      };
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error ?? new Error('IndexedDB no está disponible.'));
    });
  }
  async list() {
    const db = await this.open();
    return new Promise<TerritorialScenario[]>((resolve, reject) => {
      const request = db.transaction(LAB_STORE_NAME).objectStore(LAB_STORE_NAME).getAll();
      request.onsuccess = () => {
        try { resolve(request.result.map(importScenario)); } catch (error) { reject(error); }
        db.close();
      };
      request.onerror = () => reject(request.error);
    });
  }
  async save(scenario: TerritorialScenario) {
    const db = await this.open();
    return new Promise<void>((resolve, reject) => {
      const transaction = db.transaction(LAB_STORE_NAME, 'readwrite');
      transaction.objectStore(LAB_STORE_NAME).put(importScenario(scenario));
      transaction.oncomplete = () => { db.close(); resolve(); };
      transaction.onerror = () => reject(transaction.error);
    });
  }
  async remove(id: string) {
    const db = await this.open();
    return new Promise<void>((resolve, reject) => {
      const transaction = db.transaction(LAB_STORE_NAME, 'readwrite');
      transaction.objectStore(LAB_STORE_NAME).delete(id);
      transaction.oncomplete = () => { db.close(); resolve(); };
      transaction.onerror = () => reject(transaction.error);
    });
  }
}
