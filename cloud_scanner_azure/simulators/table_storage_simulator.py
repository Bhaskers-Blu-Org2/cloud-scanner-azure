from cloud_scanner.contracts.table_storage import TableStorage
from cloud_scanner.contracts.resource import Resource
from cloud_scanner.contracts.resource_storage_factory import register_resource_storage
from cloud_scanner.helpers import entry_storage


@register_resource_storage("simulator", lambda: TableStorageSimulator())
class TableStorageSimulator(TableStorage):

    def __init__(self):
        self._data = dict()

        self._resources = [
            { "id": '/resources/type1/resource1', "accountId": "account1", "type": "Microsoft.Storage/virtualMachine", "name": "resource1", "providerType": "simulator", "location": "location1"},
            { "id": '/resources/type1/resource2', "accountId": "account2", "type": "Microsoft.Storage/virtualMachine", "name": "resource2", "providerType": "simulator", "location": "location2"},
            { "id": '/resources/type1/resource3', "accountId": "account2", "type": "Microsoft.Storage/virtualMachine", "name": "resource3", "providerType": "simulator", "location": "location3"},
            { "id": '/resources/type1/resource4', "accountId": "account3", "type": "Microsoft.Storage/virtualMachine", "name": "resource4", "providerType": "simulator", "location": "location4"},
            { "id": '/resources/type1/resource5', "accountId": "account4", "type": "Microsoft.Storage/virtualMachine", "name": "resource5", "providerType": "simulator", "location": "location5"},
        ]

    # entry is of json type
    def write(self, resource):
        entry = resource.to_dict()
        prepared = entry_storage.EntryOperations.prepare_entry_for_insert(entry)
        key = entry['PartitionKey'] + '-' + entry['RowKey']
        self._data[key] = prepared

    def query(self, partition_key, row_key):
        task = self._data[partition_key + '-' + row_key]
        return task

    def query_list(self):
        return [Resource(resource) for resource in self._resources]

    def delete(self, partition_key, row_key):
        del self._data[partition_key + '-' + row_key]
