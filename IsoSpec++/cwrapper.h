/*
 *   Copyright (C) 2015-2019 Mateusz Łącki and Michał Startek.
 *
 *   This file is part of IsoSpec.
 *
 *   IsoSpec is free software: you can redistribute it and/or modify
 *   it under the terms of the Simplified ("2-clause") BSD licence.
 *
 *   IsoSpec is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *
 *   You should have received a copy of the Simplified BSD Licence
 *   along with IsoSpec.  If not, see <https://opensource.org/licenses/BSD-2-Clause>.
 */

#pragma once

#define ISOSPEC_ALGO_LAYERED 0
#define ISOSPEC_ALGO_ORDERED 1
#define ISOSPEC_ALGO_THRESHOLD_ABSOLUTE 2
#define ISOSPEC_ALGO_THRESHOLD_RELATIVE 3
#define ISOSPEC_ALGO_LAYERED_ESTIMATE 4


#ifdef __cplusplus
extern "C" {
#else
#include <stdbool.h>
#endif

void * setupIso(int             dimNumber,
                const int*      isotopeNumbers,
                const int*      atomCounts,
                const double*   isotopeMasses,
                const double*   isotopeProbabilities);

double getLightestPeakMassIso(void* iso);
double getHeaviestPeakMassIso(void* iso);
double getMonoisotopicPeakMassIso(void* iso);
double getModeLProbIso(void* iso);
double getModeMassIso(void* iso);
double getTheoreticalAverageMassIso(void* iso);


void deleteIso(void* iso);

#define ISOSPEC_C_FN_HEADER(generatorType, dataType, method)\
dataType method##generatorType(void* generator);

#define ISOSPEC_C_FN_HEADER_GET_CONF_SIGNATURE(generatorType)\
void method##generatorType(void* generator);

#define ISOSPEC_C_FN_HEADERS(generatorType)\
ISOSPEC_C_FN_HEADER(generatorType, double, mass) \
ISOSPEC_C_FN_HEADER(generatorType, double, lprob) \
ISOSPEC_C_FN_HEADER(generatorType, double, prob) \
ISOSPEC_C_FN_HEADER_GET_CONF_SIGNATURE(generatorType) \
ISOSPEC_C_FN_HEADER(generatorType, bool, advanceToNextConfiguration) \
ISOSPEC_C_FN_HEADER(generatorType, void, delete)




//______________________________________________________THRESHOLD GENERATOR
void* setupIsoThresholdGenerator(void* iso,
                                 double threshold,
                                 bool _absolute,
                                 int _tabSize,
                                 int _hashSize);
ISOSPEC_C_FN_HEADERS(IsoThresholdGenerator)


//______________________________________________________LAYERED GENERATOR
void* setupIsoLayeredGenerator(void* iso,
                               int _tabSize,
                               int _hashSize);
ISOSPEC_C_FN_HEADERS(IsoLayeredGenerator)

//______________________________________________________ORDERED GENERATOR
void* setupIsoOrderedGenerator(void* iso,
                               int _tabSize,
                               int _hashSize);
ISOSPEC_C_FN_HEADERS(IsoOrderedGenerator)



void* setupThresholdFixedEnvelope(void* iso,
                              double threshold,
                              bool absolute,
                              bool get_confs,
                              bool get_lprobs,
                              bool get_masses,
                              bool get_probs);

void deleteThresholdFixedEnvelope(void* tabulator);

const double* massesThresholdFixedEnvelope(void* tabulator);
const double* lprobsThresholdFixedEnvelope(void* tabulator);
const double* probsThresholdFixedEnvelope(void* tabulator);
const int*    confsThresholdFixedEnvelope(void* tabulator);
int confs_noThresholdFixedEnvelope(void* tabulator);



void* setupTotalProbFixedEnvelope(void* iso,
                              double taget_coverage,
                              bool optimize,
                              bool get_confs,
                              bool get_lprobs,
                              bool get_masses,
                              bool get_probs);

void deleteTotalProbFixedEnvelope(void* tabulator);

const double* massesTotalProbFixedEnvelope(void* tabulator);
const double* lprobsTotalProbFixedEnvelope(void* tabulator);
const double* probsTotalProbFixedEnvelope(void* tabulator);
const int*    confsTotalProbFixedEnvelope(void* tabulator);
int confs_noTotalProbFixedEnvelope(void* tabulator);

void freeReleasedArray(void* array);

void deleteTotalProbFixedEnvelope(void* tabulator);

const double* massesTotalProbFixedEnvelope(void* tabulator);
const double* lprobsTotalProbFixedEnvelope(void* tabulator);
const double* probsTotalProbFixedEnvelope(void* tabulator);
const int*    confsTotalProbFixedEnvelope(void* tabulator);
int confs_noTotalProbFixedEnvelope(void* tabulator);

void* setupFixedEnvelope(double* masses, double* probs, size_t size, bool mass_sorted, bool prob_sorted, double total_prob);
void deleteFixedEnvelope(void* tabulator, bool releaseEverything);

const double* massesFixedEnvelope(void* tabulator);
const double* lprobsFixedEnvelope(void* tabulator);
const double* probsFixedEnvelope(void* tabulator);
const int*    confsFixedEnvelope(void* tabulator);
int confs_noFixedEnvelope(void* tabulator);

double wassersteinDistance(void* tabulator1, void* tabulator2);
void* addEnvelopes(void* tabulator1, void* tabulator2);
void* convolveEnvelopes(void* tabulator1, void* tabulator2);

double getTotalProbOfEnvelope(void* envelope);
void scaleEnvelope(void* envelope, double factor);
void normalizeEnvelope(void* envelope);
void* binnedEnvelope(void* envelope, double width, double middle);
void* linearCombination(void* const * const envelopes, const double* intensities, size_t count);

void sortEnvelopeByMass(void* envelope);
void sortEnvelopeByProb(void* envelope);



#ifdef __cplusplus
}
#endif

