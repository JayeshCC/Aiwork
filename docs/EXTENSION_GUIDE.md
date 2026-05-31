# Extension Guide

AIWork is currently an alpha-stage reference implementation. This guide records the work required before deployment-oriented claims are appropriate. It is not a deployment runbook.

## Current Boundaries

- The Flask server is a local demonstration API.
- The Kafka adapter is a mock interface.
- The Redis backend is a stub.
- The OpenVINO adapter is a placeholder interface.
- The timing benchmark is simulated.
- The repository does not currently include a container definition.

## OpenVINO Extension Work

Before describing OpenVINO support as acceleration:

1. Add the OpenVINO runtime as an optional dependency.
2. Load and compile a real model.
3. Execute inference against real inputs.
4. Add integration tests around supported devices and failure cases.
5. Measure performance with a documented workload, hardware configuration, software versions, and reproducible command.

## Kafka Extension Work

Before describing Kafka support as distributed messaging:

1. Add an optional Kafka client dependency.
2. Implement serialization, producer delivery handling, and consumer groups.
3. Define offset and retry behavior.
4. Test against a real broker.
5. Document worker lifecycle and failure recovery.

## Redis Extension Work

Before describing Redis as a state backend:

1. Add a Redis client behind the existing state-manager boundary.
2. Define serialization and key lifetime behavior.
3. Handle connection failures explicitly.
4. Test persistence and cross-process visibility against a real Redis instance.

## API Hardening Work

Before describing the Flask API as deployable:

1. Replace generic submitted-task handlers with an explicit registry or allowlist.
2. Add durable state and queueing.
3. Add authentication, authorization, rate limiting, and request limits.
4. Replace daemon-thread execution with managed workers.
5. Add deployment configuration and operational tests.

## Packaging and Deployment Work

Add and verify a reproducible packaging or container path before documenting deployment commands. Any future deployment guide should be tested from a clean checkout.
