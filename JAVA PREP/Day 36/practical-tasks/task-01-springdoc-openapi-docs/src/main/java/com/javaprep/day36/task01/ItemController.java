package com.javaprep.day36.task01;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

// TODO(Day36-task01): group the endpoints: @Tag(name = "Items", description = "Item catalogue")
@RestController
@RequestMapping("/api/items")
public class ItemController {

    private static final Map<Long, Item> ITEMS = Map.of(
            1L, new Item(1, "Laptop", 999.0),
            2L, new Item(2, "Mouse", 19.5));

    // TODO(Day36-task01): @Operation(summary = "List all items")
    @GetMapping
    public List<Item> list() {
        return ITEMS.values().stream().sorted(java.util.Comparator.comparingLong(Item::id)).toList();
    }

    // TODO(Day36-task01): @Operation(summary = "Find an item by id") and @ApiResponse(responseCode = "200", description = "Item found") and @ApiResponse(responseCode = "404", description = "Item not found")
    @GetMapping("/{id}")
    public ResponseEntity<Item> get(@PathVariable long id) {
        Item item = ITEMS.get(id);
        return item == null ? ResponseEntity.notFound().build() : ResponseEntity.ok(item);
    }
}
