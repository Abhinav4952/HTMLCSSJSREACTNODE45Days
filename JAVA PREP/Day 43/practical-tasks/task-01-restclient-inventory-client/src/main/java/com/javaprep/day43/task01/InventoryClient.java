package com.javaprep.day43.task01;

import java.util.Optional;
import org.springframework.web.client.RestClient;

/** Calls the Inventory service. The RestClient is injected (base URL already configured). */
public class InventoryClient {

    private final RestClient restClient;

    public InventoryClient(RestClient restClient) {
        this.restClient = restClient;
    }

    /**
     * GET /inventory/{sku}  ->  {"sku":"ABC","available":7}
     * 404 -> Optional.empty(); 5xx or I/O failure -> InventoryUnavailableException.
     */
    public Optional<Integer> availableStock(String sku) {
        // TODO(Day43-task01): use restClient.get().uri("/inventory/{sku}", sku).retrieve()...body(StockResponse.class)
        // TODO(Day43-task01): map 404, 5xx and ResourceAccessException as described above
        throw new UnsupportedOperationException("TODO(Day43-task01): implement availableStock");
    }
}
