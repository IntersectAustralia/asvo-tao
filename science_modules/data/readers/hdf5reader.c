#include "hdf5.h"
#include <string.h>

#define MAX_FIELDS_COUNT 500
#define MAX_PATH_LENGTH  200

herr_t get_info(hid_t loc_id, const char *name, void *opdata);
hid_t file;

char fields[MAX_FIELDS_COUNT][MAX_PATH_LENGTH];
char path[MAX_PATH_LENGTH];
int counter = 0;

int main (int argc, char *argv[]) {
    if (argc < 2) {
        printf("please specify an input file.\n");
        return 0;
    } else {
        file = H5Fopen(argv[1], H5F_ACC_RDONLY, H5P_DEFAULT);
    }
    
    herr_t status;
    hid_t dataset, space, memspace; 
    hid_t spaces[MAX_FIELDS_COUNT];
    hid_t datasets[MAX_FIELDS_COUNT];
    hsize_t dims[2];
    hsize_t offset[1];
    hsize_t slice[1];
    int size, i, j, k;
    double out_buff_double[0];
    int out_buff_int[0];

    // Print out header
    status = H5Giterate(file, "/", NULL, get_info, NULL);
    printf("# ");
    for (i = 0; i < counter; i++) {
        printf("%s", fields[i]);
        if (i < counter-1) {
            printf(", ");
        }
    }
    printf("\n");

    // Read dimension of the first dataset in the file and assume this for all
    // datasets
    dataset = H5Dopen(file, fields[10], H5P_DEFAULT);
    space = H5Dget_space(dataset);
    size = H5Sget_simple_extent_dims(space, dims, NULL);

    // Open datasets for simultaneous reading
    for (j = 0; j < counter; j++) {
        datasets[j] = H5Dopen(file, fields[j], H5P_DEFAULT);
        spaces[j] = H5Dget_space(datasets[j]);
    }

    // Print out data
    slice[0] = 1;
    memspace = H5Screate_simple(1, slice, NULL);
    for (k = 0; k < dims[0]; k++) {
        offset[0] = k;
        for (j = 0; j < counter; j++) {
            status = H5Sselect_elements(spaces[j], H5S_SELECT_SET, 1, offset);
            status = H5Dread(datasets[j], H5T_NATIVE_DOUBLE, memspace, 
                spaces[j], H5P_DEFAULT, out_buff_double);
            printf("%e ", out_buff_double[0]);
        }
        printf("\n");
    }

    status = H5Fclose (file);

    return 0;
}

herr_t get_info(hid_t loc_id, const char *name, void *opdata) {
    H5O_info_t infobuf;
    herr_t status;
    char _path[200];
    H5Oget_info_by_name(loc_id, name, &infobuf, H5P_DEFAULT);
    switch (infobuf.type) {
        case H5O_TYPE_GROUP:
            strcpy(path, "/");
            strcat(path, name);
            strcat(path, "/");
            status = H5Giterate(file, name, NULL, get_info, NULL);
            strcpy(path, "");
            break;
        case H5O_TYPE_DATASET:
            strcpy(_path, path);
            strcat(_path, name);
            strcpy(fields[counter], _path);
            counter++;
            break;
        case H5O_TYPE_NAMED_DATATYPE:
            break;
        default:
            break;
    }
    return 0;
 }
