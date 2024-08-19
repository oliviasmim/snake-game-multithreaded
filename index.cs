using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

class Program
{
    static readonly object[] mtx = new object[5];
    static readonly Queue<int>[] speedUpdates = new Queue<int>[5];
    static readonly SemaphoreSlim collisionSemaphore = new SemaphoreSlim(1, 1);
    static readonly Barrier startBarrier = new Barrier(6);
    static readonly int[] positions = new int[5];
    static readonly int[] speeds = new int[5];
    static bool gameEnded = false;

    static void Main()
    {
        for (int i = 0; i < 5; i++)
        {
            mtx[i] = new object();
            speedUpdates[i] = new Queue<int>();
            positions[i] = 0;
            speeds[i] = new Random().Next(1, 10);
        }

        Task[] tasks = new Task[7];
        for (int i = 0; i < 5; i++)
        {
            int id = i;
            tasks[i] = Task.Run(() => Spaceship(id));
        }
        tasks[5] = Task.Run(CheckCollisions);
        tasks[6] = Task.Run(CheckEndGame);

        Task.WaitAll(tasks);
    }

    static void Spaceship(int id)
    {
        startBarrier.SignalAndWait();

        for (int i = 0; i < 100 && !gameEnded; i++)
        {
            lock (mtx[id])
            {
                if (speedUpdates[id].Count > 0)
                {
                    speeds[id] = speedUpdates[id].Dequeue();
                }
                positions[id] += speeds[id];
            }
            Thread.Sleep(1000);
        }
    }

    static void CheckCollisions()
    {
        startBarrier.SignalAndWait();

        while (!gameEnded)
        {
            collisionSemaphore.Wait();
            // Check for collisions...
            collisionSemaphore.Release();

            Thread.Sleep(1000);
        }
    }

    static void CheckEndGame()
    {
        startBarrier.SignalAndWait();

        while (true)
        {
            lock (mtx[0])
            {
                if (gameEnded)
                {
                    // Check if the game has ended...
                    break;
                }
            }
            Thread.Sleep(1000);
        }
    }
}