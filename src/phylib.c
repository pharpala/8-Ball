#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "phylib.h"

phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos) {
        
    // Allocate memory for new phylib_object
    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));
    
    // return if malloc wasnt successful
    if (new_object == NULL) {
        return NULL;
    }

    // Set type of object to PHYLIB_STILL_BALL
    new_object->type = PHYLIB_STILL_BALL;

    // Set object information
    new_object->obj.still_ball.number = number;
    new_object->obj.still_ball.pos = *pos;

    return new_object;
}


phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc) {

    // Allocate memory for new phylib_object
    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));

    // Check if malloc was successful
    if (new_object == NULL) {
        return NULL;
    }

    // Set type of the object to PHYLIB_ROLLING_BALL
    new_object->type = PHYLIB_ROLLING_BALL;

    // Set object information
    new_object->obj.rolling_ball.number = number;
    new_object->obj.rolling_ball.pos = *pos; 
    new_object->obj.rolling_ball.vel = *vel; 
    new_object->obj.rolling_ball.acc = *acc;

    return new_object;
}

phylib_object *phylib_new_hole(phylib_coord *pos) {

    // Get memory for new phylib_object
    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));

    // Check if malloc was successful
    if (new_object == NULL) {
        return NULL;
    }

    // Set type of object to PHYLIB_HOLE
    new_object->type = PHYLIB_HOLE;

    // Set object information
    new_object->obj.hole.pos = *pos;

    return new_object;
}

phylib_object *phylib_new_hcushion(double y) {

    // Get memory for new phylib_object
    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));

    // Check if malloc was successful
    if (new_object == NULL) {
        return NULL;
    }

    // Set type of object to PHYLIB_HCUSHION
    new_object->type = PHYLIB_HCUSHION;

    // Set object information
    new_object->obj.hcushion.y = y;

    return new_object;
}

phylib_object *phylib_new_vcushion(double x) {

    // Get memory for new phylib_object
    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));

    // Check if malloc was successful
    if (new_object == NULL) {
        return NULL;
    }

    // Set type of object to PHYLIB_VCUSHION
    new_object->type = PHYLIB_VCUSHION;

    // Set object information
    new_object->obj.vcushion.x = x;

    return new_object;
}

phylib_table *phylib_new_table(void) {

    // Get memory for new phylib_table
    phylib_table *new_table = (phylib_table *)malloc(sizeof(phylib_table));

    // Check if malloc was successful
    if (new_table == NULL) {
        return NULL;
    }

    new_table->time = 0.0;

    // Allocate and initialize objects using phylib_new_* functions
    new_table->object[0] = phylib_new_hcushion(0.0);
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // Holes
    phylib_coord hole_pos;

    // Corner holes
    hole_pos.x = 0.0;
    hole_pos.y = 0.0;
    new_table->object[4] = phylib_new_hole(&hole_pos);

    hole_pos.x = 0.0;
    hole_pos.y = PHYLIB_TABLE_WIDTH;
    new_table->object[5] = phylib_new_hole(&hole_pos);

    hole_pos.x = 0.0;
    hole_pos.y = PHYLIB_TABLE_LENGTH;
    new_table->object[6] = phylib_new_hole(&hole_pos);

    hole_pos.x = PHYLIB_TABLE_WIDTH;
    hole_pos.y = 0.0;
    new_table->object[7] = phylib_new_hole(&hole_pos);

    // Midway between top and bottom holes
    hole_pos.x = PHYLIB_TABLE_WIDTH;
    hole_pos.y = PHYLIB_TABLE_WIDTH;
    new_table->object[8] = phylib_new_hole(&hole_pos);

    hole_pos.x = PHYLIB_TABLE_WIDTH;
    hole_pos.y = PHYLIB_TABLE_LENGTH; 
    new_table->object[9] = phylib_new_hole(&hole_pos);

    // Set the remaining pointers to NULL
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; ++i) {
        new_table->object[i] = NULL;
    }

    return new_table;
}


// Part 2 starts here
void phylib_copy_object(phylib_object **dest, phylib_object **src) {
    // Check if src points to NULL
    if (*src == NULL) {
        *dest = NULL;
        return;
    }

    // Allocate memory for new phylib_object
    *dest = (phylib_object *)malloc(sizeof(phylib_object));

    // Check if malloc was successful
    if (*dest == NULL) {
        return;
    }

    // Use memcpy to copy the contents of the object from src to dest
    memcpy(*dest, *src, sizeof(phylib_object));
}

phylib_table *phylib_copy_table(phylib_table *table) {
    // Check if table pointer is NULL
    if (table == NULL) {
        return NULL;
    }

    // Allocate memory for new phylib_table
    phylib_table *new_table = (phylib_table *)malloc(sizeof(phylib_table));

    // Check if malloc was successful
    if (new_table == NULL) {
        return NULL;
    }

    memcpy(new_table,table,sizeof(phylib_table));

    for(int i=0; i<PHYLIB_MAX_OBJECTS; i++) {
        if(table->object[i] != NULL) {
            phylib_copy_object(&new_table->object[i], &table->object[i]);
        } else {
            new_table->object[i] = NULL;
        }
    }

    // Return the address of new memory location
    return new_table;
}

void phylib_add_object(phylib_table *table, phylib_object *object) {
    // Check if table or pointer are NULL
    if (table == NULL || object == NULL) {
        return;
    }

    // Iterate over the array in the table until NULL pointer is found
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        if (table->object[i] == NULL) {
            // Assign NULL pointer to address of object

            table->object[i] = object;
            break; 
        }
    }
}

void phylib_free_table(phylib_table *table) {
    // Check if table pointer is NULL
    if (table == NULL) {
        return;
    }

    // Free every non-NULL pointer in the array
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        if (table->object[i] != NULL) {
            free(table->object[i]);
            table->object[i] = NULL;
        }
    }

    // Free the table
    free(table);
}

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2) {
    phylib_coord result;
    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;
    return result;
}

double phylib_length(phylib_coord c) {
    // Calculate the length using the Pythagorean theorem
    double length_squared = c.x * c.x + c.y * c.y;

    return sqrt(length_squared);
}

double phylib_dot_product(phylib_coord a, phylib_coord b) {
    return a.x * b.x + a.y * b.y;
}

double phylib_distance(phylib_object *obj1, phylib_object *obj2) {

    if (obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0; // obj1 must be a PHYLIB_ROLLING_BALL
    }

    double distance = 0.0;

    // Get distance based on the type of obj2
    switch (obj2->type) {
        case PHYLIB_ROLLING_BALL:{
            distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos)) - PHYLIB_BALL_DIAMETER; 
            break;
        }

        case PHYLIB_STILL_BALL: {
            distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos)) - PHYLIB_BALL_DIAMETER; 
            break;
        }

        case PHYLIB_HOLE: {
            distance = phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos)) - PHYLIB_HOLE_RADIUS; 
            break;
        }

        case PHYLIB_HCUSHION: {
            double dx = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y);
            distance = dx - PHYLIB_BALL_RADIUS;
            break;
        }

        case PHYLIB_VCUSHION: {
            double dy = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x);
            distance = dy - PHYLIB_BALL_RADIUS;
            break;
        }
        
        default:
            return -1.0; // Invalid obj2 type
    }

    return distance;
}


// Part 3 starts here
void phylib_roll(phylib_object *new, phylib_object *old, double time) {

    // Check if new and old are PHYLIB_ROLLING_BALLs even though we assume it will always be
    if (new == NULL || old == NULL || new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) {
        return;
    }

    // Update positions
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time +
                                   0.5 * old->obj.rolling_ball.acc.x * time * time;
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time +
                                   0.5 * old->obj.rolling_ball.acc.y * time * time;

    // Update velocities
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;

    // Check for changes in sign and set velocities and accelerations to zero if needed
    if ((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }

    if ((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0) {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

unsigned char phylib_stopped(phylib_object *object) {
    
    // Check if the ball stopped
    if (phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON) {

        // Reset vel and acc
        object->obj.still_ball.pos = object->obj.rolling_ball.pos;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        object->obj.rolling_ball.vel.x = 0.0;
        object->obj.rolling_ball.vel.y = 0.0;
        object->obj.rolling_ball.acc.x = 0.0;
        object->obj.rolling_ball.acc.y = 0.0;
        object->type = PHYLIB_STILL_BALL;

        return 1; // Conversion worked
    }

    return 0; // Ball hasnt stopped
}

void phylib_bounce(phylib_object **a, phylib_object **b) {
    // Assume a is a rolling ball so no checking for anything else
    phylib_coord r_ab;            
    phylib_coord v_rel;
    
    // Check the type of object
    switch ((*b)->type) {
        case PHYLIB_HCUSHION:
            // Reverse y velocity bc we hit a hcushion and acceleration of obj a
            (*a)->obj.rolling_ball.vel.y = -((*a)->obj.rolling_ball.vel.y);
            (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.acc.y);
            break;

        case PHYLIB_VCUSHION:
            // Reverse x velocity and acceleration of obj a bc we hit a vcushion
            (*a)->obj.rolling_ball.vel.x = -((*a)->obj.rolling_ball.vel.x);
            (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.acc.x);
            break;
        
        case PHYLIB_HOLE:
            free(*a);
            *a = NULL;
            break; 

        case PHYLIB_STILL_BALL:
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;

        case PHYLIB_ROLLING_BALL:

            // Get r_ab
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

            // Get v_rel
            v_rel= phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

            // Get length of r_ab
            double r_ab_length = phylib_length(r_ab);

            // Get n vector
            phylib_coord n;
            n.x = r_ab.x / r_ab_length;
            n.y = r_ab.y / r_ab_length;

            // Get v_rel_n, dot product of v_rel
            double v_rel_n = phylib_dot_product(v_rel, n);

            // Get velocities of a and b
            (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

            (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

            // Get the speed of a and b
            double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
            double speed_b = phylib_length((*b)->obj.rolling_ball.vel);

            // Check if speed is greater than PHYLIB_VEL_EPSILON
            if (speed_a > PHYLIB_VEL_EPSILON) {
                // Set acc of a
                (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.vel.x / speed_a) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.vel.y / speed_a) * PHYLIB_DRAG;
            }

            if (speed_b > PHYLIB_VEL_EPSILON) {
                // Set acc of b
                (*b)->obj.rolling_ball.acc.x = -(((*b)->obj.rolling_ball.vel.x) / speed_b) * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = -(((*b)->obj.rolling_ball.vel.y) / speed_b) * PHYLIB_DRAG; 
            }
    }
}

unsigned char phylib_rolling(phylib_table *t) {

    unsigned char rolling_count = 0;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            rolling_count++;
        }
    }

    return rolling_count;
}


phylib_table *phylib_segment(phylib_table *table) {

    // Check for ROLLING_BALLs on table
    if (phylib_rolling(table) == 0) {
        return NULL;
    }
    

    phylib_table *segmentTable = phylib_copy_table(table);
    double segmentTime = PHYLIB_SIM_RATE;
    double distan;
    while(segmentTime <= PHYLIB_MAX_TIME){ 

        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            if( segmentTable->object[i] != NULL && segmentTable->object[i]->type == PHYLIB_ROLLING_BALL){
            // perform roll on each object
            phylib_roll(segmentTable->object[i],table->object[i],segmentTime);    
            }
        }

        // make separate for loops for each function because it works better and debugs easier 
        for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
            for(int j = 0; j < PHYLIB_MAX_OBJECTS; j++){
                    if( i != j && segmentTable->object[i] != NULL && segmentTable->object[i]->type == PHYLIB_ROLLING_BALL 
                                                                                      && segmentTable->object[j] != NULL) 
                    {
                        distan = phylib_distance(segmentTable->object[i],segmentTable->object[j]); 
                        if(distan < 0.0){
                            // Collision checking
                            phylib_bounce(&(segmentTable->object[i]),&(segmentTable->object[j]));
                            segmentTable->time += segmentTime;
                            return segmentTable;
                        }
                    }
                }
                if(segmentTable->object[i] != NULL && segmentTable->object[i]->type == PHYLIB_ROLLING_BALL && phylib_stopped(segmentTable->object[i]))
                {
                    segmentTable->time += segmentTime;
                    return segmentTable; 
                }
            }
            segmentTime += PHYLIB_SIM_RATE;
        } 
      
        return segmentTable;
}


char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }

    switch (object->type)
    {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
            break;

        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;
        
        case PHYLIB_HOLE:
            snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
            break;

        case PHYLIB_HCUSHION:
            snprintf( string, 80,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
            break;
            case PHYLIB_VCUSHION:
            snprintf( string, 80,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
            break;
    }

    return string;
}
