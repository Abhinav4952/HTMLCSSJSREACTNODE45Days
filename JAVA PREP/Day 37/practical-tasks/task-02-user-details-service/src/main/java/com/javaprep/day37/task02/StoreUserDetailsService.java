package com.javaprep.day37.task02;

import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

public class StoreUserDetailsService implements UserDetailsService {

    private final UserStore store;

    public StoreUserDetailsService(UserStore store) {
        this.store = store;
    }

    /**
     * Unknown user -> UsernameNotFoundException.
     * Otherwise build Spring's User with: username, the stored hash, roles (as "ROLE_x" authorities via .roles(...)),
     * and disabled(true) when the record is not enabled. Usernames are case-insensitive (store handles it).
     */
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // TODO(Day37-task02): look up the record and map it to UserDetails
        throw new UnsupportedOperationException("TODO(Day37-task02): look up the record and map it to UserDetails");
    }
}
