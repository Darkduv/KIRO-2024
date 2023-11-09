# Couts

def cost_cable(c_f, c_l, l_e):
    return c_f + c_l * l_e

# No failure cost

def power_generated_to_sub(pi_t, nb_t):
    return pi_t * nb_t

def cable_capacity_from_sub(rate_sub, rate_link_to_land):
    return min(rate_sub, rate_link_to_land)

def curtailing_of_sub(pi_t, nb_t, rate_sub, rate_link_to_land):
    sub_input = power_generated_to_sub(pi_t, nb_t)
    sub_max_output = cable_capacity_from_sub(rate_sub, rate_link_to_land)
    return max(0, sub_input - sub_max_output)

#------ Puis on fait la somme là dessus
